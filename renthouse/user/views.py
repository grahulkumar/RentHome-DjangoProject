from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login, logout
from .models import CustomUser

#user's home page
def user_home(request):
    return render(request,'user/user_home.html')

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

#find home
def find_home(request):
    return render(request,'user/find_home.html')
