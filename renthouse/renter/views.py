from django.shortcuts import render,redirect
from .models import HomeDetails

#renter's home page
def renter_home(request):
    data={}
    get_image=HomeDetails.objects.all()
    data['homedetails']=get_image
    return render(request,'renter/renter_home.html',context=data)

#add home here
def add_home(request):
    if(request.method == 'POST'):
        add=request.POST['add']
        add1=request.POST['add1']
        state=request.POST['state']
        city=request.POST['city']
        pincode=request.POST['pincode']
        price=request.POST['price']
        about=request.POST['about']
        condition=request.POST['condition']
        image_file = request.FILES['image']
        if(add=="" or add1=="" or price=="" or city==""):
            print("all fields required")
        else:
            addHome=HomeDetails.objects.create(image=image_file,add=add,add1=add1,state=state,city=city,pincode=pincode,about=about,condition=condition,price=price)
            addHome.save()
            print("renter saved successfully")
            return redirect('renter-home')
    return render(request,'renter/add_home.html')