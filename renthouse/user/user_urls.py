from django.urls import path

#import user's views.py
from user import views 

urlpatterns = [
    path('',views.user_home, name="home"),
    path('sign-in/',views.user_signin, name="sign-in"),
    path('sign-up/',views.user_signup , name="sign-up"),
    path('renter-sign-up/',views.renter_signup, name="renter-sign-up"),
    path('logout/',views.user_logout, name="logout"),
    path('profile/',views.profile, name="profile"),
    path('result/',views.home_result, name="result"),
    path('home-details/<int:id>&<int:d>',views.home_details, name="details"),
    path('rent-summary/<int:id>&<int:d>',views.rent_summary, name="rent-summary"),
    path('rental-history/',views.rental_history, name="rental-history"),

]