from django.shortcuts import render,redirect, get_object_or_404
from .models import HomeDetails
from user.models import CustomUser

#renter's home page
def renter_home(request):
    data={}
    if not request.user.is_authenticated:
        return redirect("home")
    else:
        user_id=request.user.id
        get_data=HomeDetails.objects.filter(rid_id=user_id)
        data['homedetails']=get_data
        
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
        people=request.POST['people']
        about=request.POST['about']
        condition=request.POST['condition']
        image_file = request.FILES['image']
        # Validate required fields
        if not all([add, add1, state, city, pincode, price, people,about,condition,image_file]):
            print("All fields are required")
        else:
            #get renter id
            user=request.get.id
            user_id=CustomUser.objects.get(id=user)
            addHome=HomeDetails.objects.create(image=image_file,add=add,add1=add1,state=state,city=city,pincode=pincode,about=about,condition=condition,price=price, people=people,rid_id=user_id)
            addHome.save()
            print("renter saved successfully")
            return redirect('renter-home')
    return render(request,'renter/add_home.html')

#edit home here
def edit_home(request,pk):
    data={}
    homedetails= get_object_or_404(HomeDetails, id=pk)
    data['home']=homedetails
    if(request.method == 'POST'):
        add=request.POST['add']
        add1=request.POST['add1']
        state=request.POST['state']
        city=request.POST['city']
        pincode=request.POST['pincode']
        price=request.POST['price']
        people=request.POST['people']
        about=request.POST['about']
        condition=request.POST['condition']
        #update image
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            homedetails.image = image_file 
        
        # Validate required fields
        if not all([add, add1, state, city, pincode, price, people,about,condition]):
            print("All fields are required")
        else:
          # Update the home details
            homedetails.add = add
            homedetails.add1 = add1
            homedetails.state = state
            homedetails.city = city
            homedetails.pincode = pincode
            homedetails.price = price
            homedetails.people = people
            homedetails.about = about
            homedetails.condition = condition
            homedetails.save()  # Save the updated home details            print("house updated successfully")
            return redirect('renter-home')
    return render(request,'renter/edit_home.html',context=data)

#delete home here
def delete_home(request,pk):
    homedetails= get_object_or_404(HomeDetails, id=pk)
    homedetails.delete()
    print("deleted home successfully")
    return redirect('renter-home')
   