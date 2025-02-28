import django_filters
from .models import Tour

class TourFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte', label="Цена от")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte', label="Цена до")
    duration_min = django_filters.NumberFilter(field_name="duration", lookup_expr='gte', label="Мин. длительность")
    duration_max = django_filters.NumberFilter(field_name="duration", lookup_expr='lte', label="Макс. длительность")
    country = django_filters.ModelChoiceFilter(queryset=Tour.objects.values_list('country__name', flat=True).distinct(), label="Страна")


    class Meta:
        model = Tour
        fields = ['country', 'price_min', 'price_max', 'duration_min', 'duration_max']

        # class TourFilter(django_filters.FilterSet):
        #     hot_tours = django_filters.BooleanFilter(field_name="old_price", lookup_expr="isnull", exclude=True,
        #                                              label="Горящие туры")
        #
        #     class Meta:
        #         model = Tour
        #         fields = ['country', 'price_min', 'price_max', 'duration_min', 'duration_max', 'hot_tours']

