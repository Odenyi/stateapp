from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager, Permission,Group

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provide a valid email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    def create_user(self, email= None, password = None, **etxra_fields):
        etxra_fields.setdefault('is_staff', False)
        etxra_fields.setdefault('is_superuser', False)

        return self. _create_user(email,password,**etxra_fields)
    def create_superuser(self, email= None, password = None, **etxra_fields):
        etxra_fields.setdefault('is_staff', True)
        etxra_fields.setdefault('is_superuser', True)

        return self. _create_user(email,password,**etxra_fields)



class User(AbstractUser,PermissionsMixin):
    email = models.EmailField(blank=True, default="",unique=True)
    username =  models.CharField(max_length=66, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True,null=True)

    objects = CustomUserManager()
    USERNAME_FIELD ="email"
    EMAIL_FIELD  = "email",
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username or self.email.split("@")[0]


  

    def __str__(self):
        return self.get_short_name()

    
class PropertyListing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=11, decimal_places=2)
    location = models.ForeignKey('Location',on_delete=models.SET_NULL, null=True, blank=True)
    offer_type = models.ForeignKey('OfferType',on_delete=models.SET_NULL, null=True,blank=True)
    property_type = models.ForeignKey('PropertyType', on_delete=models.SET_NULL, null=True,blank=True)
    main_image = models.ImageField(upload_to='property_images/')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)


    def __str__(self):
        return self.title




class MoreImage(models.Model):
    property = models.ForeignKey(PropertyListing, on_delete=models.CASCADE,blank=True,null=True)
    image = models.ImageField(upload_to='property_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Image {self.id} - Property {self.property.title}"






class PropertyFeature(models.Model):
    property = models.OneToOneField(PropertyListing,on_delete=models.CASCADE,null=True, blank=True)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    size = models.IntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Property: {self.property.title} - Bedrooms: {self.bedrooms} - Bathrooms: {self.bathrooms}"



# sold /rent/sale 
class OfferType(models.Model):
    offer_type =models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.offer_type


class PropertyType(models.Model):
    property_type =models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.property_type




class ShowInterest(models.Model):
    property = models.ForeignKey(PropertyListing,on_delete=models.CASCADE, null=True,blank=True)
    username = models.CharField(max_length=64,null=True,blank=True)
    email =models.CharField(max_length=64)
    phone = models.CharField(max_length=15)
    message = models.TextField(null=True,blank=True)
    url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def __str__(self):
        return f"Interest {self.id} - Property {self.property}"


class Amenities(models.Model):
    amenities = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.amenities
class PropertyAmenities(models.Model):
    property = models.ForeignKey(PropertyListing,on_delete=models.CASCADE, blank=True, null=True)
    amenities =  models.ForeignKey(Amenities,on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "f {self.amenities}  {self.property} "


class County(models.Model):
    county_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.county_name


class Location(models.Model):
    county = models.ForeignKey(County,on_delete=models.CASCADE, blank=True, null=True)
    location_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.location_name




class Blog(models.Model):
    property_type = models.ForeignKey(PropertyType,on_delete=models.SET_NULL, null=True,blank=True)
    title = models.CharField(max_length=64,null=True,blank=True)
    image = models.ImageField(upload_to='blog_images/')
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)


def __str__(self):
        return f"Blog {self.id} - title {self.title}"

class Video(models.Model):
    property_type = models.ForeignKey(PropertyType,on_delete=models.SET_NULL, null=True,blank=True)
    title = models.CharField(max_length=64,null=True,blank=True)
    video = models.FileField(upload_to='property_videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)

class GeneralMessages(models.Model):
    
    username = models.CharField(max_length=64,null=True,blank=True)
    email =models.CharField(max_length=64,null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    message = models.TextField(null=True,blank=True)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE, null=True,blank=True)
    message_type = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def __str__(self):
        return f"General Messages {self.id} - Message {self.message}"



