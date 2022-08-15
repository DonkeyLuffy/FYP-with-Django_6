from dataclasses import fields
import django_filters
from django_filters import CharFilter, NumberFilter, RangeFilter, DateFilter, TimeRangeFilter
from .models import *


# class ProfileFilter(django_filters.FilterSet):
    # user__first_name = CharFilter(label='First Name', lookup_expr='icontains')
    # user__last_name = CharFilter(label='Last Name', lookup_expr='icontains')
    # weight = NumberFilter(label='Weight', lookup_expr='gte')
    # shoe_size = RangeFilter(label='Shoe Size')
    # class Meta:
    #     model = Profile
    #     fields = '__all__'
        # fields = ['user__first_name', 'user__last_name', 'weight', 'shoe_size','size_type']


class ProfileFilter(django_filters.FilterSet):
    user__first_name = CharFilter(label='First Name', lookup_expr='icontains')
    user__last_name = CharFilter(label='Last Name', lookup_expr='icontains')
    weight = NumberFilter(label='Weight', lookup_expr='gte')
    shoe_size = RangeFilter(label='Shoe Size')
    class Meta:
        model = Profile
        fields = '__all__'
        fields = ['user__first_name', 'user__last_name', 'weight', 'shoe_size', 'size_type']

class DeviceDataFilter(django_filters.FilterSet):
    date = DateFilter(label='Date', lookup_expr='icontains' )
    time = TimeRangeFilter(label='Time Range(HH:MM:SS)')
    class Meta:
        model = DeviceData
        fields = '__all__'
        exclude = ['user']

class AdminDataFilter(django_filters.FilterSet):
    date = DateFilter(label='Date', lookup_expr='icontains' )
    time = TimeRangeFilter(label='Time Range(HH:MM:SS)')
    class Meta:
        model = DeviceData
        fields = '__all__'
        exclude = ['user']
        
