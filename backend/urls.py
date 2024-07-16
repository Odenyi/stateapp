from django.urls import path
from . import views

# to be edited to desired routes
urlpatterns = [
    path('dashboard/', views.dashboard, name="admin_dashboard"),
    path('property/', views.property, name="admin_property"),
    path('propertylist/', views.propertylist, name="admin_propertylist"),
    path('rent/', views.rent, name="admin_rent"),
    path('sale/', views.sale, name="admin_sale"),
    path('featured/', views.featured, name="admin_featured"),
    path('apartment/', views.apartment, name="admin_apartment"),
    path('messages/', views.sitemessages, name="admin_messages"),
    path('blogs/', views.blogs, name="admin_blogs"),
    path('videos/', views.videos, name="admin_videos"),
    path('addblog/', views.addblog, name="admin_addblog"),
    path('addvideo/', views.addvideo, name="admin_addvideo"),

    path('addproperty/', views.admin_addproperty, name="admin_addproperty"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('adminblog-details/<int:id>/', views.blogdetails, name="adminblog-details"),
    path('adminblog-edit/<int:blogid>/', views.blogedit, name="adminblog-edit"),
    path('adminblog-delete/<int:blogid>/', views.blogdelete, name="adminblog-delete"),
    # to load location asynchronous
    path('ajax/load-location', views.load_location, name='ajax_load_location'),
     # Edit Property
    path('property/edit/<int:property_id>/', views.edit_property, name='edit_adminproperty'),

    # View Property
    path('property/view/<int:property_id>/', views.view_property, name='view_adminproperty'),
    path('signout/', views.signout, name="signout"),
    

    # Delete Property
    path('property/delete/<int:property_id>/', views.delete_property, name='delete_adminproperty'),
    path('property/delete_more_image/<int:image_id>/', views.delete_more_image, name='delete_more_image'),
    path('users/', views.user_list, name='user_list'),
    path('edit_user/<int:user_id>', views.useredit, name='edit_user'),
    path('delete_user/<int:user_id>', views.userdelete, name='delete_user'),
    path('edit_video/<int:video_id>', views.videoedit, name='edit_video'),
    path('delete_video/<int:video_id>', views.videodelete, name='delete_video')
           

   
   
]