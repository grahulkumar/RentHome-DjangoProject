from django.urls import path

#import user's views.py
from user import views 

urlpatterns = [
    path('',views.user_home),
]