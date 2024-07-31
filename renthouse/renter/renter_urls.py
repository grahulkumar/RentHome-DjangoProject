from django.urls import path
#import user's views.py
from renter import views 

urlpatterns = [
    path('',views.renter_home, name="renter-home"),
    path('add-home/',views.add_home, name="add-home"),
    path('edit-home/<int:pk>',views.edit_home, name="edit-home"),
    path('delete-home/<int:pk>',views.delete_home, name="delete-home"),
] 
