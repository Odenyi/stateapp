from django.shortcuts import render,get_object_or_404, redirect
from .models import *
from django.http import JsonResponse
import os
from django.contrib.auth import authenticate,login,logout
from .forms import UserRegistrationForm
from django.db.models import Case, When, F, Value, IntegerField
from django.db.models import Q
from datetime import datetime,date, timedelta
import calendar
import requests
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import random
from django.core.exceptions import ObjectDoesNotExist
from random import sample
# Create your views here.

# admin dashboard
@login_required(login_url='signin')
def dashboard(request):

    # get data from weather api
    api_key = '4ab36b73f3d740659cc193943233008'
    city = 'Nairobi'
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'

    response = requests.get(url)
    weather_data = response.json()
    # sunrise_time = weather_data['sun']
    # sunset_time = weather_data['sunset']
    current_time = datetime.now()

    
    
    # day and night
    # sunrise_datetime = datetime.fromtimestamp(sunrise_time)
    # sunset_datetime = datetime.fromtimestamp(sunset_time)
    #  Calculate the current month
    current_month = datetime.now().month
    previous_month = datetime.now().month-1
    year = datetime.now().year
    if(previous_month==0):
        year = datetime.now().year-1
        previous_month = 12

    # get message count()
    message_count = ShowInterest.objects.all().count()
    # Filter properties created in the current month and year
    court_properties = PropertyListing.objects.filter(date_created__month=current_month,date_created__year=datetime.now().year).count()
    
    # compare prorties from previous month and current in percentage
    percentage_cpm =round(court_properties/(court_properties+PropertyListing.objects.filter(date_created__month=previous_month,date_created__year=year).count())*100,1) if court_properties+PropertyListing.objects.filter(date_created__month=previous_month,date_created__year=year).count() > 0 else 0.0 

    percentage_cpy = round(PropertyListing.objects.filter(date_created__year=datetime.now().year).count()/(PropertyListing.objects.filter(date_created__year=datetime.now().year).count() + PropertyListing.objects.filter(date_created__year=datetime.now().year-1).count())*100,1) if PropertyListing.objects.filter(date_created__year=datetime.now().year).count() + PropertyListing.objects.filter(date_created__year=datetime.now().year-1).count() > 0 else 0.0

    # Calculate the total count of all properties
    total_properties = PropertyListing.objects.all().count()

    # Calculate property count where type is rent
    rent_properties_count = PropertyListing.objects.filter(offer_type__offer_type__iexact='rent').count()
    # compare this month and last month rent
    rent_cpm = round(PropertyListing.objects.filter(offer_type__offer_type__iexact='rent',date_created__month=current_month,date_created__year=datetime.now().year).count()/(PropertyListing.objects.filter(offer_type__offer_type__iexact='rent',date_created__month=previous_month,date_created__year=year).count()+PropertyListing.objects.filter(offer_type__offer_type__iexact='rent',date_created__month=current_month,date_created__year=datetime.now().year).count())*100,1) if PropertyListing.objects.filter(offer_type__offer_type__iexact='rent',date_created__month=previous_month,date_created__year=year).count()+PropertyListing.objects.filter(offer_type__offer_type__iexact='rent',date_created__month=current_month,date_created__year=datetime.now().year).count() > 0 else 0.0
    
    # Calculate property sum of price where type is rented or sold and updated_at is in the current year
    rented_sold_properties_sum = PropertyListing.objects.filter(
    offer_type__offer_type__in=['Rented', 'Sold'],
    date_updated__year=datetime.now().year
    ).count()
    rented_sold_properties_sum_lstyr= PropertyListing.objects.filter(
    offer_type__offer_type__in=['Rented', 'Sold'],
    date_updated__year=datetime.now().year-1
    ).count()

    
    # Get today's date
    today = date.today()

        # Calculate yesterday's date
    yesterday = today - timedelta(days=1)

    # Calculate the start and end of last week
    last_week_end = today - timedelta(days=today.weekday() + 1)
    last_week_start = last_week_end - timedelta(days=6)

    # Calculate the start and end of last month
    last_month_end = date(today.year, today.month, 1) - timedelta(days=1)
    last_month_start = date(today.year, today.month - 1, 1)

    # Calculate the start and end of last year
    last_year_end = date(today.year - 1, 12, 31)
    last_year_start = date(today.year - 1, 1, 1)

    # Query for properties rented or sold yesterday
    rented_sold_properties_yesterday = PropertyListing.objects.filter(
        offer_type__offer_type__in=['Rented', 'Sold'],
        date_updated__date=yesterday
    ).count()
    # properties which are apartment or furnished apartments
    apartment_properties = PropertyListing.objects.filter(
        property_type__property_type__in=['apertment', 'furnished apartment'],
        
    ).count()

    bungalow_properties = PropertyListing.objects.filter(
        property_type__property_type__iexact='bungalow',
        
    ).count()

    mansion_properties = PropertyListing.objects.filter(
        property_type__property_type__iexact='mansion',
        
    ).count()
    villa_properties = PropertyListing.objects.filter(
        property_type__property_type__iexact='villa',
        
    ).count()
    
   
    # rented by yesterday
    rented_properties_yesterday = PropertyListing.objects.filter(
        offer_type__offer_type__iexact='rented',
        date_updated__date=yesterday
    ).count()

    # rented by last month
    rented_properties_last_month = PropertyListing.objects.filter(
        offer_type__offer_type__iexact='Rented',
        date_updated__range=(last_month_start, last_month_end)
    ).count()
    # sold last year
    sold_properties_last_year = PropertyListing.objects.filter(
        offer_type__offer_type__iexact='sold',
        date_updated__range=(last_year_start, last_year_end)
    ).count()

     # sold by yesterday
    sold_properties_yesterday = PropertyListing.objects.filter(
        offer_type__offer_type__iexact='sold',
        date_updated__date=yesterday
    ).count()

    # sold by last month
    sold_properties_last_month = PropertyListing.objects.filter(
        offer_type__offer_type__iexact='sold',
        date_updated__range=(last_month_start, last_month_end)
    ).count()

    # rented last year
    rented_properties_last_year = PropertyListing.objects.filter(
        offer_type__offer_type__iexact='rented',
        date_updated__range=(last_year_start, last_year_end)
    ).count()



    # Query for properties rented or sold last week
    rented_sold_properties_last_week = PropertyListing.objects.filter(
        offer_type__offer_type__in=['Rented', 'Sold'],
        date_updated__range=(last_week_start, last_week_end)
    ).count()

    # Query for properties rented or sold last month
    rented_sold_properties_last_month = PropertyListing.objects.filter(
        offer_type__offer_type__in=['Rented', 'Sold'],
        date_updated__range=(last_month_start, last_month_end)
    ).count()

    # Query for properties rented or sold last year
    rented_sold_properties_last_year = PropertyListing.objects.filter(
        offer_type__offer_type__in=['Rented', 'Sold'],
        date_updated__range=(last_year_start, last_year_end)
    ).count()

    # Get the start and end of the current week
    current_week_start = today - timedelta(days=today.weekday())
    current_week_end = current_week_start + timedelta(days=6)

    # Get the start and end of the current month
    current_month_start = date(today.year, today.month, 1)
    current_month_end = date(today.year, today.month + 1, 1) - timedelta(days=1)


     
    # rented by today
    rented_properties_today = PropertyListing.objects.filter(
        offer_type__offer_type__iexact='rented',
        date_updated__date=today
    ).count()

    # rented by this month
    rented_properties_this_month = PropertyListing.objects.filter(
        offer_type__offer_type__iexact='Rented',
        date_updated__range=(current_month_start, current_month_end)
    ).count()
    # rented  this year
    rented_properties_this_year = PropertyListing.objects.filter(
        offer_type__offer_type__iexact='rented',
        date_updated__year=datetime.now().year
    ).count()

    # sold by today
    sold_properties_today = PropertyListing.objects.filter(
        offer_type__offer_type__iexact='sold',
        date_updated__date=today
    ).count()

    # sold by this month
    sold_properties_this_month = PropertyListing.objects.filter(
        offer_type__offer_type__iexact='Sold',
        date_updated__range=(current_month_start, current_month_end)
    ).count()
    # sold  this year
    sold_properties_this_year = PropertyListing.objects.filter(
        offer_type__offer_type__iexact='sold',
        date_updated__year=datetime.now().year
    ).count()

    # rented percentage this year today this month
    rented_properties_this_month_pc = round(rented_properties_this_month/(rented_properties_this_month+rented_properties_last_month)*100,1) if rented_properties_this_month+rented_properties_last_month > 0 else 0.0
    rented_properties_this_year_pc = round(rented_properties_this_year/(rented_properties_this_year+rented_properties_last_year)*100,1) if rented_properties_this_year+rented_properties_last_year > 0 else 0.0
    rented_properties_this_today_pc = round(rented_properties_today/(rented_properties_today+rented_properties_yesterday)*100,1) if rented_properties_today + rented_properties_yesterday > 0 else 0.0

    # sold percentage this year today this month
    sold_properties_this_month_pc = round(sold_properties_this_month/(sold_properties_this_month+sold_properties_last_month)*100,1) if sold_properties_this_month+sold_properties_last_month > 0 else 0.0
    sold_properties_this_year_pc = round(sold_properties_this_year/(sold_properties_this_year+sold_properties_last_year)*100,1) if sold_properties_this_year+sold_properties_last_year > 0 else 0.0 
    sold_properties_this_today_pc = round(sold_properties_today/(sold_properties_today+sold_properties_yesterday)*100,1) if sold_properties_today+sold_properties_yesterday > 0 else 0.0
   
    # Query for properties rented or sold this month
    rented_sold_properties_month = PropertyListing.objects.filter(
        offer_type__offer_type__in=['Rented', 'Sold'],
        date_updated__range=(current_month_start, current_month_end)
    ).count()

    # Query for properties rented or sold this week
    rented_sold_properties_week = PropertyListing.objects.filter(
        offer_type__offer_type__in=['Rented', 'Sold'],
        date_updated__range=(current_week_start, current_week_end)
    ).count()

    # Query for properties rented or sold today
    rented_sold_properties_today = PropertyListing.objects.filter(
        offer_type__offer_type__in=['Rented', 'Sold'],
        date_updated__date=today
    ).count()


    # Rented sold percentage this year today this month
    rented_sold_properties_today_pc = round(rented_sold_properties_today/(rented_sold_properties_today+rented_sold_properties_yesterday)*100,1) if rented_sold_properties_today+rented_sold_properties_yesterday > 0 else 0.0
    rented_sold_properties_month_pc = round(rented_sold_properties_month/(rented_sold_properties_month+rented_sold_properties_last_month)*100,1) if rented_sold_properties_month+rented_sold_properties_last_month > 0 else 0.0
    

    #compare this year and last year
    rentedsold_percentage = round(rented_sold_properties_sum/(rented_sold_properties_sum_lstyr+rented_sold_properties_sum)*100,1) if rented_sold_properties_sum_lstyr+rented_sold_properties_sum > 0 else 0.0


    context = {
        'court_properties': court_properties,
        'total_properties': total_properties,
        'rent_properties_count': rent_properties_count,
        'rented_sold_properties_sum': rented_sold_properties_sum,
        'year':datetime.now().year,
        'month':calendar.month_name[current_month],
        'percentage_cpm':percentage_cpm,
        'percentage_cpy':percentage_cpy,
        'rent_cpm':rent_cpm,
        'rented_sold_properties_month':rented_sold_properties_month,
        'rented_sold_properties_week':rented_sold_properties_week,
        'rentedsold_percentage':rentedsold_percentage,
        'rented_sold_properties_today':rented_sold_properties_today,
        'rented_sold_properties_yesterday': rented_sold_properties_yesterday,
        'rented_sold_properties_last_week': rented_sold_properties_last_week,
        'rented_sold_properties_last_month': rented_sold_properties_last_month,
        'rented_sold_properties_last_year': rented_sold_properties_last_year,
        'rented_properties_today':rented_properties_today,
        'rented_properties_last_month': rented_properties_last_month,
        'rented_properties_last_year': rented_properties_last_year,
        'rented_properties_this_month_pc':rented_properties_this_month_pc,
        'rented_properties_this_year_pc':rented_properties_this_year_pc,
        'rented_properties_this_today_pc':rented_properties_this_today_pc,
        'sold_properties_this_month_pc':sold_properties_this_month_pc,
        'sold_properties_this_year_pc':sold_properties_this_year_pc,
        'sold_properties_this_today_pc':sold_properties_this_today_pc,
        'rented_sold_properties_month_pc':rented_sold_properties_month_pc,
        'rented_sold_properties_today_pc':rented_sold_properties_today_pc,
        'apartment_properties':apartment_properties,
        'weather_data':weather_data,
        'bungalow_properties':bungalow_properties,
        'mansion_properties':mansion_properties,
        'villa_properties':villa_properties,
        'message_count':message_count

    }

    return render(request,"index.html",context)

# 3 colum property
# property context
@login_required(login_url='signin')
def property(request):
    # order by first rent then sale the others follow
    ordering_case = Case(
        When(offer_type__offer_type='Rent', then=Value(1)),
        When(offer_type__offer_type='Sale', then=Value(2)),
        default=Value(3), output_field=IntegerField()
    )
    properties = PropertyListing.objects.all().order_by(ordering_case, '-date_updated')
    propertycontext = {'properties': properties,}
    return render(request,"property-list3.html", propertycontext)

# list property,
@login_required(login_url='signin')
def propertylist(request):
    # order by first rent then sale the others follow
    ordering_case = Case(
        When(offer_type__offer_type='Rent', then=Value(1)),
        When(offer_type__offer_type='Sale', then=Value(2)),
        default=Value(3), output_field=IntegerField()
    )
    properties = PropertyListing.objects.all().order_by(ordering_case, '-date_updated')
    propertycontext = {'properties': properties,}
    return render(request,"property-list.html",propertycontext)

# for rent
@login_required(login_url='signin')
def rent(request):
    rent_properties = PropertyListing.objects.filter(offer_type__offer_type__in=['Rented', 'rent']).order_by('-date_updated')
    propertycontext = {'properties': rent_properties,}
    return render(request,"rent.html",propertycontext )

# videos
@login_required(login_url='signin')
def videos(request):
    # Retrieve a list of users from your Videos model
    videos = Video.objects.all()

    # Create a context dictionary to pass data to the template
    context = {'videos': videos}

    # Render the template with the Videos data
    return render(request, 'video.html', context)

# for sale
@login_required(login_url='signin')
def sale(request):
    sale_properties = PropertyListing.objects.filter(offer_type__offer_type__in=['Sale', 'Sold']).order_by('-date_updated')
    propertycontext = {'properties': sale_properties,}
    return render(request,"sale.html",propertycontext)

# featured properties
@login_required(login_url='signin')
def featured(request):
    featured_properties = PropertyListing.objects.filter(offer_type__offer_type__iexact="featured").order_by('-date_updated')
    propertycontext = {'properties': featured_properties,}
    return render(request,"featured.html",propertycontext)

# furnished 
@login_required(login_url='signin')
def apartment(request):
    # order by first rent then sale the others follow
    ordering_case = Case(
        When(offer_type__offer_type='Rent', then=Value(1)),
        When(offer_type__offer_type='Sale', then=Value(2)),
        default=Value(3), output_field=IntegerField()
    )
    properties = PropertyListing.objects.filter(property_type__property_type__in=['apartment', 'furnished apartment']).order_by(ordering_case, '-date_updated')
    context ={"properties":properties}
    return render(request,"apartment.html",context)

# add property
@login_required(login_url='signin')
def admin_addproperty(request):
    if request.method == "POST":
        
        title = request.POST.get('propertyname')
        property_description = request.POST.get('propertydescription', '')
        property_location = request.POST.get('propertylocation', '')
        property_offertype = request.POST.get('radio1', '')
        property_price = request.POST.get('propertyprice', '')
        propertytype = request.POST.get('propertytype', '')
        selected_amenities = request.POST.getlist('propertyamenities', [])
        images = request.FILES.getlist('propertyimages', [])
        property_bathrooms = request.POST.get('propertybathrooms')
        property_bedrooms = request.POST.get('propertybedrooms')
        property_size = request.POST.get('propertysize')

        
       

        


      
        location = Location.objects.get(id=property_location)
        offer_type = OfferType.objects.get(id=property_offertype)
        p_type = PropertyType.objects.get(id=propertytype)


        property_listing = PropertyListing.objects.create(title=title,description=property_description,price=property_price,location=location, offer_type=offer_type,property_type=p_type,posted_by= request.user)
        # Save the first image as the main_image
        if images:
            main_image = images[0]
            property_listing.main_image = main_image
            property_listing.save()
        # Save the rest of the images in MoreImages
        for image in images[1:]:
            MoreImage.objects.create( property=property_listing, image=image)
        for amenity in selected_amenities:
            property_amenity = Amenities.objects.get(id=amenity)
            PropertyAmenities.objects.create( property=property_listing, amenities=property_amenity )
        # save property size and property bathrooms and bedrooms
        PropertyFeature.objects.create(property = property_listing, bedrooms = property_bedrooms, bathrooms = property_bathrooms, size = property_size)


        return JsonResponse({'success': 'Property saved successfully.'}, status=200)
            
    property_type = PropertyType.objects.all()
    county = County.objects.all()
    amenities = Amenities.objects.all()
    offers = OfferType.objects.all()
    context = {'property_type':property_type, 'counties':county,'amenities':amenities,'offers':offers}
    return render(request, "add-property.html",context)

# signup
def signup(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "user saved succesful.")
            return redirect('signin')  # Redirect to the login page
 
  
   
    return render(request, "sign-up.html", {"form": form})
# signin
def signin(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request,username=username, password= password)
        if user is not None and user.is_superuser == 1:
            login(request, user)
            return redirect('admin_dashboard')
        elif user is not None and user.is_superuser == 0:
            messages.error(request,"You are not allowed")

        else:
            messages.error(request,"Username or Password is incorrect")

    return render(request, "sign-in.html")
# signout
@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')


def blogs_generalmessages(request):
    pass
# messages
@login_required(login_url='signin')
def sitemessages(request):
    # Fetch messages from GeneralMessages model
    general_messages = GeneralMessages.objects.all()
    
    # Fetch messages from ShowInterest model
    show_interest_messages = ShowInterest.objects.all()
    
    # Combine both sets of messages
    all_messages = list(general_messages) + list(show_interest_messages)
    
    # Sort the combined messages by their created_at timestamp in descending order
    all_messages.sort(key=lambda x: x.created_at, reverse=True)
    
    # Number of messages to display per page
    items_per_page = 10 # Change this to the number of messages you want per page
    
    # Create a Paginator instance
    paginator = Paginator(all_messages, items_per_page)
    
    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')
    
    # Get the Page object for the current page
    page_messages = paginator.get_page(page_number)
    
    context = {"messagesp": page_messages}
    
    return render(request, "mail-inbox.html", context)

# blogs
@login_required(login_url='signin')
def blogs(request):
    blogs = Blog.objects.annotate(message_count=Count('generalmessages')).order_by('-created_at', '-message_count')
    popularblogs = Blog.objects.annotate(
    message_count=Count('generalmessages')
).order_by('-message_count')[:2]
    # Get all PropertyType objects
    all_property_types = PropertyType.objects.all()

    # Shuffle the queryset to randomize the order
    randomized_property_types = list(all_property_types)
    random.shuffle(randomized_property_types)

    # Get the first 5 randomized property types
    p_type_random = randomized_property_types[:5]

    badge_colors = ["success", "info", "warning", "danger", "primary", "secondary"]

    for p_type in p_type_random:
        p_type.badge_color = sample(badge_colors, 1)[0]


    items_per_page = 3

    paginator = Paginator(blogs, items_per_page)
    page_number = request.GET.get('page')
    page_blogs = paginator.get_page(page_number)

    context = {"blogs":page_blogs,'popularblogs':popularblogs,'p_type_random':p_type_random,'badge_colors':badge_colors}
    return render(request,"blog-list.html",context)
# blog details
@login_required(login_url='signin')
def blogdetails(request,id):
    blog = get_object_or_404(Blog, id=id)
    messages1=blog.generalmessages_set.all().order_by("-created_at")

    messagecount = messages1.count()
    # Number of items to show per page
    items_per_page = 3

    paginator = Paginator(messages1, items_per_page)
    page_number = request.GET.get('page')
    page_messages = paginator.get_page(page_number)
    context = {"blog":blog,"blogs":page_messages,"messagecount":messagecount}
    return render(request,"adminblog-details.html",context)

@login_required(login_url='signin')
def addvideo(request):
    if request.method == "POST":
         videotitle = request.POST.get('videotitle')
         videotype = request.POST.get('videotype')
         mainvideo = request.FILES.getlist('mainvideo', [])
         print(mainvideo)
         p_type = PropertyType.objects.get(id=videotype)

         Video.objects.create(property_type = p_type, title = videotitle, video = mainvideo[0],posted_by = request.user)
         return JsonResponse({'success': 'Blog saved successfully.'}, status=200)

    property_type = PropertyType.objects.all().order_by('property_type')
    
    return render(request,"add-video.html",{'property_type':property_type})

    
@login_required(login_url='signin')
def addblog(request):
    if request.method == "POST":
         blogtitle = request.POST.get('blogtitle')
         blogtype = request.POST.get('blogtype')
         blogdescription = request.POST.get('blogdescription')
         mainimage = request.FILES.getlist('blogimage', [])
         p_type = PropertyType.objects.get(id=blogtype)

         Blog.objects.create(property_type = p_type, title = blogtitle, image = mainimage[0], description=blogdescription,posted_by=request.user)
         return JsonResponse({'success': 'Blog saved successfully.'}, status=200)



    property_type = PropertyType.objects.all().order_by('property_type')
    
    return render(request,"blog-post.html",{'property_type':property_type})
    

# fetch location 
@login_required(login_url='signin')
def load_location(request):
    county_id = request.GET.get('county')
    location = Location.objects.filter(county=county_id).order_by('location_name')
    return render(request, 'components/location_dropdown_list_options.html', {'locations': location})
@login_required(login_url='signin')
def edit_property(request, property_id):
    property = get_object_or_404(PropertyListing, id=property_id)
    property_type = PropertyType.objects.all()
    county = County.objects.all()
    amenities = Amenities.objects.all()
    offers = OfferType.objects.all()
    more_images=property.moreimage_set.all()
    amenityids=property.propertyamenities_set.values_list('amenities_id', flat=True)
    # Handle the editing logic here
    if request.method == 'POST':
        # Update the property based on the form data
        propertytitle = request.POST.get('propertyname')
        property_description = request.POST.get('propertydescription', '')
        property_location = request.POST.get('propertylocation', '')
        property_offertype = request.POST.get('radio1', '')
        property_price = request.POST.get('propertyprice', '')
        propertytype = request.POST.get('propertytype', '')
        selected_amenities = request.POST.getlist('propertyamenities', [])
        moreimages = request.FILES.getlist('moreimages', [])
        mainimage = request.FILES.getlist('mainimage', [])
        property_bathrooms = request.POST.get('propertybathrooms')
        property_bedrooms = request.POST.get('propertybedrooms')
        property_size = request.POST.get('propertysize')
        if len(mainimage) != 0:
            if property.main_image:
                os.remove(property.main_image.path)
            property.main_image = mainimage[0]

        # objects with relationships with main
        location = Location.objects.get(id=property_location)
        offer_type = OfferType.objects.get(id=property_offertype)
        p_type = PropertyType.objects.get(id=propertytype)
        #  Get all amenities_id associated with the property ID
        existing_amenities_ids = PropertyAmenities.objects.filter(property_id=property_id).values_list('amenities_id', flat=True)
        
        # Get the queryset of existing amenities to delete
        amenities_to_delete = PropertyAmenities.objects.filter(
            property_id=property_id,
            amenities_id__in=existing_amenities_ids.exclude(amenities_id__in=selected_amenities)
        ).delete()

    

      
        # Create and save new PropertyAmenities instances for selected_amenities
        for amenity_id in selected_amenities:
            amenity_id_int = int(amenity_id)
            if amenity_id_int not in existing_amenities_ids:
              
                property_amenity = PropertyAmenities(property_id=property_id, amenities_id=amenity_id_int)
                property_amenity.save()

        # Check if PropertyFeature exists for this property
        try:
            property_feature = PropertyFeature.objects.get(property=property)
        except PropertyFeature.DoesNotExist:
            # If PropertyFeature does not exist, create a new one
            property_feature = PropertyFeature(property=property, bedrooms=0, bathrooms=0, size=0)
        property_feature.bathrooms = property_bathrooms
        property_feature.bedrooms = property_bedrooms
        property_feature.size = property_size
        property_feature.save()

        property.title = propertytitle
        property.description = property_description
        property.price =property_price
        property.location =location
        property.offer_type = offer_type
        property.property_type = p_type
        property.save()

        for image in moreimages:
            MoreImage.objects.create( property=property, image=image)

        return JsonResponse({'success': 'Property Updated successfully.'}, status=200)
        

        
    
    context = {
        'adminproperty': property,'property_type':property_type, 'counties':county,'amenities':amenities,'offers':offers,'property_amenities':amenityids, 'more_images':more_images
    }
    
    return render(request, 'edit_adminproperty.html', context)
@login_required(login_url='signin')
def view_property(request, property_id):
    property = get_object_or_404(PropertyListing, id=property_id)
    amenities = Amenities.objects.all()
    offers = OfferType.objects.all()
    more_images=property.moreimage_set.all()
    property_type = PropertyType.objects.all()
    
    amenityids=property.propertyamenities_set.all()
    
    context = {
        'adminproperty': property,'property_type':property_type,'offers':offers,'property_amenities':amenityids, 'more_images':more_images
    }
    return render(request, 'view_adminproperty.html', context)

@login_required(login_url='signin')
def user_list(request):
     # Retrieve a list of users from your User model
    users = User.objects.all()

    # Create a context dictionary to pass data to the template
    context = {'users': users}

    # Render the template with the user data
    return render(request, 'user_list.html', context)
# user edit
@login_required(login_url='signin')
def useredit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        useremail = request.POST.get('useremail')

        new_password = request.POST.get('userpassword')
        role = request.POST.get('user_type')

        user.username = username
        user.email = useremail
        
        # Update the user's password
        if(new_password):
             user.set_password(new_password)
        
        # Update the user's role
        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False
        
        user.save()
        return JsonResponse({'success': 'User updated successfully.'}, status=200)
    
    context = {'edituser': user}
    return render(request, 'edit_user.html', context)
# user delete
def userdelete(request,user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        try:
            user.delete()
        # Redirect to property list or other page
            return JsonResponse({'success': True})
            
        except property.DoesNotExist:
            return JsonResponse({'success': False})  

@login_required(login_url='signin')
def delete_property(request, property_id):
    property = get_object_or_404(PropertyListing, id=property_id)
    
    if request.method == 'DELETE':
        try:
            os.remove(property.main_image.path)
            more_images=property.moreimage_set.all()
            for image in more_images:
                if image.image:
                    os.remove(image.image.path)
            property.delete()
        # Redirect to property list or other page
            return JsonResponse({'success': True})
        except property.DoesNotExist:
            return JsonResponse({'success': False})  
    
    

# delete more image on update
@login_required(login_url='signin')
def delete_more_image(request, image_id):
    if request.method == 'DELETE':

        try:
            image = MoreImage.objects.get(id=image_id)
            os.remove(image.image.path)
            image.delete()
            return JsonResponse({'success': True})
        except MoreImage.DoesNotExist:
            return JsonResponse({'success': False})
@login_required(login_url='signin')
def blogedit(request, blogid):
    blog = get_object_or_404(Blog, id=blogid)
    property_type = PropertyType.objects.all()
    if request.method == 'POST':
        try:
            blogtitle = request.POST.get('blogtitle')
            blogtype = request.POST.get('blogtype')
            blogdescription = request.POST.get('blogdescription')
            maineditimage = request.FILES.getlist('blogeditimage', [])
           
            p_type = PropertyType.objects.get(id=blogtype)
            if len(maineditimage) != 0:
                if blog.image:
                    os.remove(blog.image.path)
                blog.image = maineditimage[0]
            blog.title = blogtitle
            blog.property_type =p_type
            blog.description = blogdescription
            blog.save()
            return JsonResponse({'success': True})
        except blog.DoesNotExist:
            return JsonResponse({'success': False})
    context = {'blog':blog,'property_type':property_type}
    return render(request,"adminblogedit.html",context)
@login_required(login_url='signin')
def blogdelete(request, blogid):
    pass


# edit  video
@login_required(login_url='signin')
def videoedit(request,video_id):
    video = get_object_or_404(Video, id=video_id)
    property_type = PropertyType.objects.all()
    if request.method == 'POST':
        try:
            videotitle = request.POST.get('videotitle')
            videotype = request.POST.get('videotype')
            maineditimage = request.FILES.getlist('videoeditimage', [])
           
            p_type = PropertyType.objects.get(id=videotype)
            if len(maineditimage) != 0:
                if video.image:
                    os.remove(video.image.path)
                video.image = maineditimage[0]
            video.title = videotitle
            video.property_type =p_type
            video.save()
            return JsonResponse({'success': True})
        except video.DoesNotExist:
            return JsonResponse({'success': False})
    context = {'video':video,'property_type':property_type}
    return render(request,"edit-video.html",context)
@login_required(login_url='signin')
def videodelete(request,video_id):
    myvideo = get_object_or_404(Video, id=video_id)
    
    if request.method == 'POST':
        try:
            os.remove(myvideo.video.path)
            myvideo.delete()
        # Redirect to property list or other page
            return JsonResponse({'success': True})
            
        except ObjectDoesNotExist:
            return JsonResponse({'success': False})  




        

