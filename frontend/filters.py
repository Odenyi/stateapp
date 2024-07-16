import django_filters
from backend.models import *

class PropertyListingFilter(django_filters.FilterSet):
    min_area = django_filters.NumberFilter(
        field_name='property_feature__size', lookup_expr='gte'
    )
    max_area = django_filters.NumberFilter(
        field_name='property_feature__size', lookup_expr='lte'
    )
    bedrooms = django_filters.NumberFilter(
        field_name='property_feature__bedrooms', lookup_expr='exact'
    )
    bathrooms = django_filters.NumberFilter(
        field_name='property_feature__bathrooms', lookup_expr='exact'
    )
    location = django_filters.CharFilter(
        field_name='location__location_name', lookup_expr='exact'
    )
    offertype = django_filters.CharFilter(
        field_name='offer_type__offer_type', lookup_expr='exact'
    )
    class Meta:
        model = PropertyListing
        fields = {
            'price': ['range'],
        }
        exclude = ['main_image',]
