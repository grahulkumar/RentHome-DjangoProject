from django.shortcuts import render

#user's home page
def user_home(request):
    return render(request,'base.html')
