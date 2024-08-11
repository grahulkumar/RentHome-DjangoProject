from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from renter.models import HomeDetails, Rentdetails
from django.urls import reverse
from datetime import datetime, timedelta
from decimal import Decimal
from django.http import JsonResponse


# stripe
import stripe
from django.conf import settings

# from django.db.models import Q


# user's home page
def user_home(request):
    if request.method == "POST":
        city = request.POST["city"]
        state = request.POST["state"]
        fromprice = request.POST["fromprice"]
        toprice = request.POST["toprice"]
        days = request.POST["days"]
        url = (
            reverse("result")
            + f"?days={days}&fromprice={fromprice}&toprice={toprice}&city={city}&state={state}&sortby=default"
        )
        return redirect(url)
    return render(request, "user/user_home.html")


# filtering home results
def home_result(request):
    data = {}
    # Retrieve data from find home form
    days = request.GET.get("days")
    fromprice = request.GET.get("fromprice")
    toprice = request.GET.get("toprice")
    city = request.GET.get("city")
    state = request.GET.get("state")
    sortby = request.GET.get("sortby")

    # filter data
    home_data = HomeDetails.objects.filter(
        city__icontains=city,
        state=state,
        price__range=(fromprice, toprice),
        status="not rented",
    )
    # __range to find between values
    # __icontain ignore case to get value

    home_count = home_data.count()  # get result count from database

    # if data is not found according to user but it similar to location
    if not home_data:
        home = HomeDetails.objects.filter(
            city__icontains=city, state=state, status="not rented"
        )
        if not home:
            data["msg"] = "No homes found at your location !!"
        else:
            data["msg"] = (
                "No homes found based on given values but we found on your location !!"
            )
            data["per"] = "One Night"
    else:
        home = home_data

    # sorting by price
    if sortby == "high":
        home = home.order_by("-price")  #'-' for descending order
    elif sortby == "low":
        home = home.order_by("price")
    else:
        home = home

    # send data from sortby form to get sorted results
    if request.method == "POST":
        sort_by = request.POST["sortby"]
        url = (
            reverse("result")
            + f"?days={days}&fromprice={fromprice}&toprice={toprice}&city={city}&state={state}&sortby={sort_by}"
        )
        return redirect(url)

    data["count"] = home_count
    data["days"] = days
    data["homes"] = home
    data["sort"] = sortby
    return render(request, "user/results.html", context=data)


# home-details
def home_details(request, id, d):
    data = {}
    # home details from result page
    home = get_object_or_404(HomeDetails, id=id)

    # get renter name
    renter_name = get_object_or_404(CustomUser, id=home.rid_id)
    data["name"] = renter_name.name

    # if days is 1
    if d == 1:
        data["per"] = "One Night"
    data["days"] = d
    data["home"] = home
    return render(request, "user/home_details.html", context=data)


# rent summary
def rent_summary(request, id, d):
    # if user is not signed in then redirect to signin page
    if not request.user.is_authenticated:
        return redirect("sign-in")
    data = {}
    # home details from result page
    home = get_object_or_404(HomeDetails, id=id)

    # get renter name
    renter_name = get_object_or_404(CustomUser, id=home.rid_id)
    data["rname"] = renter_name.name

    # get user name
    user_id = request.user.id
    # print(user_id)
    user_name = get_object_or_404(CustomUser, id=user_id)
    data["uname"] = user_name.name

    # if days is 1
    if d == 1:
        data["per"] = "One Night"
    data["days"] = d
    data["home"] = home

    # get current date
    data["curdate"] = datetime.now()

    # total price
    total_price = home.price * Decimal(d)
    data["total"] = total_price

    # get form data
    if request.method == "POST":
        sdate = request.POST["date"]  # date format yyyy-mm-dd
        stime = request.POST["time"]  # time format hh:mm

        # combine date and time into a single datetime object
        s_date = f"{sdate} {stime}"  # format yyyy-mm-dd hh:mm
        start_date = datetime.strptime(s_date, "%Y-%m-%d %H:%M")

        # find end date by adding days in start date
        end_date = start_date + timedelta(days=d)

        url=( reverse('payment') + f'?u_id={user_id}&p_id={id}&start_date={start_date}&end_date={end_date}&total_price={total_price}')
        return redirect(url)
    return render(request, "user/rent_summary.html", context=data)

#payment
def payment(request):
    # Retrieve data from rent_summary
    u_id = request.GET.get("u_id")
    p_id = request.GET.get("p_id")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    total_price = request.GET.get("total_price")
    data={'u_id':u_id,'p_id':p_id,'start_date':start_date,'end_date':end_date,'total_price':total_price}
    
    #Save data to the database
    rentinghome=Rentdetails.objects.create(
            u_id=u_id,
            p_id=p_id,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
        )
    rentinghome.save()

    # home details from result page
    home = get_object_or_404(HomeDetails, id=p_id)
    #change status in home
    home.status="rented"
    home.save()
    
    return render(request,'user/payment.html',context=data)

# success and cancel payment
def success(request):
    return render(request, "success.html")


def cancel(request):
    return render(request, "cancel.html")


# rent history
def rental_history(request):
    # get user id
    user_id = request.user.id
    data = {}
    renthome_data = Rentdetails.objects.filter(u_id=user_id).select_related(
        "p"
    )  # join Homedetails table

    data["homes"] = renthome_data
    return render(request, "user/rental_history.html", context=data)


# auth
# sign_in page
def user_signin(request):
    data = {}
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if email == "" or password == "":
            data["msg"] = "all fields required"
        else:
            user_auth = authenticate(request, email=email, password=password)
            if user_auth is None:
                data["msg"] = "Enter correct email and password"
            else:
                login(request, user_auth)
                if hasattr(user_auth, "role"):  # Ensure role attribute exists
                    if user_auth.role == "Renter":
                        return redirect("renter-home")
                    else:
                        return redirect("home")
                else:
                    return redirect("sign-in")
    return render(request, "common/sign_in.html", context=data)


# user sign_up page
def user_signup(request):
    data = {}
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        cpassword = request.POST["cpassword"]

        # check email already present on database or not
        check_email = get_object_or_404(CustomUser, email=email)

        if name == "" or email == "" or password == "" or cpassword == "":
            data["msg"] = "all fields required"
        elif password != cpassword:
            data["msg"] = "Password doesn't match"
        elif email == check_email.email:
            data["msg"] = "Email already exist"
        else:
            user = CustomUser.objects.create(name=name, email=email, role="User")
            user.set_password(password)
            user.save()
            # print("user saved successfully")
            return redirect("sign-in")
    return render(request, "common/sign_up.html", context=data)


# renter sign_up page
def renter_signup(request):
    data = {}
    if request.method == "POST":
        rname = request.POST["name"]
        remail = request.POST["email"]
        rpassword = request.POST["password"]
        rcpassword = request.POST["cpassword"]

        # check email already present on database or not
        check_email = get_object_or_404(CustomUser, email=remail)

        if rname == "" or remail == "" or rpassword == "" or rcpassword == "":
            data["msg"] = "all fields required"
        elif rpassword != rcpassword:
            data["msg"] = "Password doesn't match"
        elif remail == check_email.email:
            data["msg"] = "Email already exist"
        else:
            renter = CustomUser.objects.create(name=rname, email=remail, role="Renter")
            renter.set_password(rpassword)
            renter.save()
            # print("renter saved successfully")
            return redirect("sign-in")
    return render(request, "common/renter_sign_up.html", context=data)


# user_logout
def user_logout(request):
    logout(request)
    return redirect("home")


# User profile section
def profile(request):
    # get user id
    user_id = request.user.id
    data = {}
    user_data=CustomUser.objects.get(id=user_id)
    data['name']=user_data.name
    data['email']=user_data.email
    return render(request, "common/profile.html",context=data)
