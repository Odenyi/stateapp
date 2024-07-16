from django.urls import path
from . import views

# to be edited to desired routes
urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('properties/', views.properties, name="properties"),
    path('propertydetail/<int:id>/', views.propertydetail, name="property_detail"),
    path('showinterest/<int:id>/', views.showinterest, name="showinterest"),
    path('fnapartments/', views.fnapartments, name="fnapartments"),
    path('blogs/', views.blog, name="blogs"),
    path('blog-details/<int:id>/', views.blogdetails, name="blog-details"),
    path('contact/', views.contact, name="contact"),
    path('savecontactmessage/', views.savecontactmessage, name="savecontactmessage"),
    
]