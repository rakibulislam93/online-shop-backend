import django_filters

from . import models

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price',lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price',lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__name',lookup_expr='iexact')
    
    class Meta:
        model = models.Product
        fields = ['min_price','max_price','category','is_available']