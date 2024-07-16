from django.shortcuts import render, get_object_or_404
from backend.models import PropertyType,PropertyListing,ShowInterest,Blog,GeneralMessages,Location
from django.http import JsonResponse
from django.db.models import Case, When, F, Value, IntegerField
from django.core.paginator import Paginator
import random
from django.db.models import Q
from django.db.models import Count
from .config import *
from .filters import PropertyListingFilter

admincontact = "0722077779"
# Create your views here.
def index(request):
    # Fetch random blogs
    
    maxpriceproperty = 0

    minpriceproperty = 0
    # Fetch the properties with the maximum and minimum prices
    max_price_property = PropertyListing.objects.order_by('-price').first()
    min_price_property = PropertyListing.objects.order_by('price').first()

    # Check if the properties exist and set the prices accordingly
    if max_price_property is not None:
        maxpriceproperty = max_price_property.price

    if min_price_property is not None:
        minpriceproperty = min_price_property.price
    random_blogs = Blog.objects.all().order_by('?')[:3]
    location_names = Location.objects.all().order_by('location_name')
    property_type = PropertyType.objects.all().order_by('property_type')
    # Get values from the form's input fields
    location = request.GET.get('location', '')
    propertytype = request.GET.get('propertytype', '')
    min_area = request.GET.get('min-area', '')
    max_area = request.GET.get('max-area', '')
    bedrooms = request.GET.get('bedrooms', '')
    bathrooms = request.GET.get('bathrooms', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    # Initialize the query
    query = Q()

    # Add conditions to the query based on form inputs
    if location:
        query &= Q(location__location_name=location)
    if propertytype:
        query &= Q(property_type__property_type=propertytype)
    if min_area:
        print(min_area)
        query &= Q(propertyfeature__size__gte=min_area)
    if max_area:
        print(max_area)
        query &= Q(propertyfeature__size__lte=max_area)
    if bedrooms:
        query &= Q(propertyfeature__bedrooms=bedrooms)
    if bathrooms:
        query &= Q(propertyfeature__bathrooms=bathrooms)
    if min_price:
        query &= Q(price__gte=min_price)
    if max_price:
        query &= Q(price__lte=max_price)
    
    # Get properties with the filter
  
    property_filter = getproperties(request).filter(query)
    
    # Number of items to show per page
    items_per_page = 12

    paginator = Paginator(property_filter, items_per_page)
    page_number = request.GET.get('page')
    page_properties = paginator.get_page(page_number)
    
    context = {
        'properties': page_properties,
        'random_blogs': random_blogs,
        'property_filter': property_filter,  # Pass the filter to the template
        'location_names':location_names,
        'location': location,
        'propertytype': propertytype,
        'min_area': min_area,
        'max_area': max_area,
        'bedrooms': bedrooms,
        'property_types':property_type,
        'bathrooms': bathrooms,
        'min_price': min_price,
        'max_price': max_price,
        'maxpriceproperty':maxpriceproperty,
        'minpriceproperty':minpriceproperty
    }
    
    return render(request, "index-two.html", context)


# about
def about(request):
    return render(request,"about.html")

# properties
def properties(request):

    maxpriceproperty = 0

    minpriceproperty = 0
     # Fetch the properties with the maximum and minimum prices
    max_price_property = PropertyListing.objects.order_by('-price').first()
    min_price_property = PropertyListing.objects.order_by('price').first()

    # Check if the properties exist and set the prices accordingly
    if max_price_property is not None:
        maxpriceproperty = max_price_property.price

    if min_price_property is not None:
        minpriceproperty = min_price_property.price
    
    location_names = Location.objects.all().order_by('location_name')
    property_type = PropertyType.objects.all().order_by('property_type')
    # Get values from the form's input fields
    location = request.GET.get('location', '')
    propertytype = request.GET.get('propertytype', '')
    min_area = request.GET.get('min-area', '')
    max_area = request.GET.get('max-area', '')
    bedrooms = request.GET.get('bedrooms', '')
    bathrooms = request.GET.get('bathrooms', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    # Initialize the query
    query = Q()

    # Add conditions to the query based on form inputs
    if location:
        query &= Q(location__location_name=location)
    if propertytype:
        query &= Q(property_type__property_type=propertytype)
    if min_area:
        print(min_area)
        query &= Q(propertyfeature__size__gte=min_area)
    if max_area:
        print(max_area)
        query &= Q(propertyfeature__size__lte=max_area)
    if bedrooms:
        query &= Q(propertyfeature__bedrooms=bedrooms)
    if bathrooms:
        query &= Q(propertyfeature__bathrooms=bathrooms)
    if min_price:
        query &= Q(price__gte=min_price)
    if max_price:
        query &= Q(price__lte=max_price)
    
    # Get properties with the filter
  
    property_filter = getproperties(request).filter(query)
    # Number of items to show per page
    items_per_page = 12

    paginator = Paginator(property_filter, items_per_page)
    page_number = request.GET.get('page')
    page_properties = paginator.get_page(page_number)
    context = {
        'properties': page_properties,
        'location_names':location_names,
        'location': location,
        'propertytype': propertytype,
        'min_area': min_area,
        'max_area': max_area,
        'bedrooms': bedrooms,
        'property_types':property_type,
        'bathrooms': bathrooms,
        'min_price': min_price,
        'max_price': max_price,
        'maxpriceproperty':maxpriceproperty,
        'minpriceproperty':minpriceproperty
        }
    return render(request,"properties-col-3.html",context)

# furnished apartments
def fnapartments(request):
    fn = "fnapartments"
    maxpriceproperty = 0

    minpriceproperty = 0
 
     # Fetch the properties with the maximum and minimum prices
    max_price_property = PropertyListing.objects.order_by('-price').first()
    min_price_property = PropertyListing.objects.order_by('price').first()

    # Check if the properties exist and set the prices accordingly
    if max_price_property is not None:
        maxpriceproperty = max_price_property.price

    if min_price_property is not None:
        minpriceproperty = min_price_property.price

    
    location_names = Location.objects.all().order_by('location_name')
    property_type = PropertyType.objects.all().order_by('property_type')
    # Get values from the form's input fields
    location = request.GET.get('location', '')
    propertytype = request.GET.get('propertytype', '')
    min_area = request.GET.get('min-area', '')
    max_area = request.GET.get('max-area', '')
    bedrooms = request.GET.get('bedrooms', '')
    bathrooms = request.GET.get('bathrooms', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    # Initialize the query
    query = Q()

    # Add conditions to the query based on form inputs
    if location:
        query &= Q(location__location_name=location)
    if propertytype:
        query &= Q(property_type__property_type=propertytype)
    if min_area:
        print(min_area)
        query &= Q(propertyfeature__size__gte=min_area)
    if max_area:
        print(max_area)
        query &= Q(propertyfeature__size__lte=max_area)
    if bedrooms:
        query &= Q(propertyfeature__bedrooms=bedrooms)
    if bathrooms:
        query &= Q(propertyfeature__bathrooms=bathrooms)
    if min_price:
        query &= Q(price__gte=min_price)
    if max_price:
        query &= Q(price__lte=max_price)
    
    # Get properties with the filter
  
    property_filter = getproperties(request,fn).filter(query)
    # Number of items to show per page
    items_per_page = 12

    paginator = Paginator(property_filter, items_per_page)
    page_number = request.GET.get('page')
    page_properties = paginator.get_page(page_number)
    context = {
        'properties': page_properties,
        'location_names':location_names,
        'location': location,
        'propertytype': propertytype,
        'min_area': min_area,
        'max_area': max_area,
        'bedrooms': bedrooms,
        'property_types':property_type,
        'bathrooms': bathrooms,
        'min_price': min_price,
        'max_price': max_price,
        'maxpriceproperty':maxpriceproperty,
        'minpriceproperty':minpriceproperty
        }
   

    return render(request,"furnishedapartments.html",context)

# blog
def blog(request):
    blogs = Blog.objects.all().order_by('-created_at')
    # number of blogs per page
    items_per_page = 12

    paginator = Paginator(blogs, items_per_page)
    page_number = request.GET.get('page')
    page_properties = paginator.get_page(page_number)
    context = {'properties': page_properties,}
   
    return render(request,"blog.html",context)

# blog details

def blogdetails(request, id):
    blog = Blog.objects.get(id=id)
    messages=blog.generalmessages_set.all().order_by("-created_at")

    messagecount = messages.count()
    # Number of items to show per page
    items_per_page = 3

    paginator = Paginator(messages, items_per_page)
    page_number = request.GET.get('page')
    page_messages = paginator.get_page(page_number)
    
    # count of property types
    property_type_counts = PropertyListing.objects.values('property_type__property_type').annotate(count=Count('id'))
   
    # get random blogs limit 3
    other_random_blogs = Blog.objects.filter(
    ~Q(id=blog.id)
).order_by('?')[:3]
   
    context = {"blog":blog,"property_type_counts":property_type_counts,"other_random_blogs":other_random_blogs,"properties":page_messages,"messagecount":messagecount}
    return render(request,"blogfend-details.html",context)


# contact
def contact(request):
    return render(request,"contact_fend.html")

def getproperties(request,propertytype="property"):
    # Create a Case expression to specify the ordering based on offer_type id
    
    ordering_case = Case(
        When(offer_type__offer_type='Rent', then=Value(1)),
        When(offer_type__offer_type='Sale', then=Value(2)),
        default=Value(3), output_field=IntegerField()
    )
     # Retrieve properties ordered by the Case expression and then by date_updated
    properties = PropertyListing.objects.all().order_by(ordering_case, '-date_updated')
    if(propertytype == "fnapartments"):
        
         # Retrieve properties ordered by the Case expression and then by date_updated
        properties = PropertyListing.objects.filter(property_type__property_type__in=['apartment', 'furnished apartment']).order_by(ordering_case, '-date_updated')
        
   
    return properties

# property detail
def propertydetail(request,id):

    try:
        property = PropertyListing.objects.get(id=id)
        
    except PropertyListing.DoesNotExist:
        # Handle the case when the object does not exist
        # For example, you can raise a 404 error
        raise Http404("Property does not exist")
    more_images=property.moreimage_set.all() 
    # get random related properties
    random_related_properties = PropertyListing.objects.filter(
    Q(property_type__property_type__iexact=property.property_type) &
    ~Q(id=property.id)
).order_by('?')[:3]
   
    
    amenityids=property.propertyamenities_set.all()
    property_type_counts = PropertyListing.objects.values('property_type__property_type').annotate(count=Count('id'))
    
        
    context = {"property":property,"more_images":more_images,"random_related_properties":random_related_properties,"property_amenities":amenityids,"property_type_counts":property_type_counts,}
    return render(request,"properties-details.html",context)

# show interest (messages from users)
# to do sent sms to both users and admins sent email to admin and users
def showinterest(request, id):
    if request.method == "POST":
        message = request.POST.get("message")
        email = request.POST.get("email")
        name = request.POST.get("name")
        number = request.POST.get("number")
        url =request.POST.get("url")

    
       
        property = get_object_or_404(PropertyListing, id=id)

        showinterest = ShowInterest.objects.create(property=property,username=name,email=email,phone=number,message=message,url = url)
        showinterest.save()
        newmessage = f"Dear Admin,\n\nA new property interest has been received for {property.title}.\n\nDetails:\nName: {name}\nEmail: {email}\nPhone: {number}\nMessage: {message}\n\nProperty URL: {url}"
        clientmessage =f"Dear {name} we have received your request one of our representatives will contact you."
        
        sendsms(admincontact, newmessage)
        response = sendsms(number, clientmessage)
        if(response.status_code != 200):
            return JsonResponse({'success': False})
        
        return JsonResponse({'success': True})
    

          # Send email notification to the admin
        subject = f"New Property Interest: {property.title}"
        message = f"Dear Admin,\n\nA new property interest has been received for {property.title}.\n\nDetails:\nName: {name}\nEmail: {email}\nPhone: {number}\nMessage: {message}\n\nProperty URL: {url}"
        from_email = 'your-email@example.com'
        recipient_list = ['admin@example.com']
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
        
        # Send response to the client
        response_data = {'success': True}
        return JsonResponse(response_data)

    return JsonResponse({'success': False})

def sendsms(number, message):
    import requests

    recipient = number  # recipient's phone number
    text = message  # message to be sent


    headers = {
        "h_api_key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "mobile": recipient,
        "response_type": "json",
        "sender_name": SHORTCODE,
        "service_id": 0,
        "message": text
    }

    response = requests.post(URL, json=payload, headers=headers)
    return response
    # response.status_code == 200:
     

def savecontactmessage(request):
     if request.method == "POST":
        message = request.POST.get("message")
        email = request.POST.get("email")
        name = request.POST.get("name")
        
        url = request.POST.get("url")
        if url == "blogcontact":
            message_type ="blog"
            blogid = request.POST.get("blogid")
            blog =  Blog.objects.get(id=blogid)

            generalmessage = GeneralMessages.objects.create(username=name,email=email,blog=blog,message=message,message_type = message_type)
            generalmessage.save()
            print("passed")
            return JsonResponse({'success': True})
        else:
            number = request.POST.get("number")
            message_type = "general"
            generalmessage = GeneralMessages.objects.create(username=name,email=email,phone=number,message=message,message_type = message_type)
            generalmessage.save()
            newmessage = f"You have new notification from {name} on contact form. Mobile {number}."
            

            response = sendsms(admincontact,  newmessage)
            if (response.status_code !=200):
                return JsonResponse({'success': False})
            return JsonResponse({'success': True})
