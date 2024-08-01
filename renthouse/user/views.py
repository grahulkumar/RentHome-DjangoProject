from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login, logout
from .models import CustomUser
from renter.models import HomeDetails
from django.urls import reverse

#user's home page
def user_home(request):
    if(request.method == 'POST'):
        city=request.POST['city']
        state = request.POST['state']
        fromprice=request.POST['fromprice']
        toprice=request.POST['toprice']
        people=request.POST['people']
        url = reverse('result') + f'?people={people}&fromprice={fromprice}&toprice={toprice}&city={city}&state={state}'
        return redirect(url)
    return render(request,'user/user_home.html')

#filtering home results
def home_result(request):
    data={}
    # Retrieve data from find home form
    city = request.GET.get('city')
    state = request.GET.get('state')
    fromprice = request.GET.get('fromprice')
    toprice = request.GET.get('toprice')
    people = request.GET.get('people')
    homes=HomeDetails.objects.filter(city__icontains=city,state=state,people__gte=people,price__range=(fromprice, toprice)) 
    #__gte to get minimum value and __range to find between values

    data['homes']=homes
    return render(request,'user/home_details.html',context=data)

#sign_in page
def user_signin(request):
    if(request.method == 'POST'):       
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        if(email=="" or password==""):
            print("all fields required")
        else:
            user_auth=authenticate(request,email=email,password=password)
            if(user_auth is None):
                print("user does not exist")
                return render(request, 'common/sign_in.html')
            else:
                login(request,user_auth)
                if hasattr(user_auth, 'role'):  # Ensure role attribute exists
                   if user_auth.role == "Renter":
                        return redirect("renter-home")
                   else:
                        return redirect("home")
                else:
                    return redirect("sign-in")
    return render(request,'common/sign_in.html')

#user sign_up page
def user_signup(request):
    if(request.method == 'POST'):
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        if(name=="" or email=="" or password=="" or cpassword==""):
            print("all fields required")
        else:
            user=CustomUser.objects.create(name=name,email=email,role="User")
            user.set_password(password)
            user.save()
            print("user saved successfully")
            return redirect("sign-in")
    return render(request,'common/sign_up.html')

#renter sign_up page
def renter_signup(request):
    if(request.method == 'POST'):
        rname=request.POST['name']
        remail=request.POST['email']
        rpassword=request.POST['password']
        rcpassword=request.POST['cpassword']
        if(rname=="" or remail=="" or rpassword=="" or rcpassword==""):
            print("all fields required")
        else:
            renter=CustomUser.objects.create(name=rname,email=remail,role="Renter")
            renter.set_password(rpassword)
            renter.save()
            print("renter saved successfully")
            return redirect("sign-in")
    return render(request,'common/renter_sign_up.html')

#user_logout
def user_logout(request):
    logout(request)
    return redirect("home")


#User profile section
def profile(request):
    return render(request,'common/profile.html')

