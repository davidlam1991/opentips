from django.forms import TextInput, DateInput
import django_filters

from .models import Post
from .choices import TIPS_SITUATION_CHOICES, FOOD_TYPE_CHOICES, JOB_TYPE_CHOICES


class PostFilter(django_filters.FilterSet):
    restaurant_name = django_filters.CharFilter(
        lookup_expr='icontains',
    )

    address = django_filters.CharFilter(
        lookup_expr='icontains',
    )

    tips_situation = django_filters.ChoiceFilter(
        choices=[('all', 'All')] + list(TIPS_SITUATION_CHOICES),
        empty_label="Tipping Policy",
        method='filter_all',
    )

    job_type = django_filters.ChoiceFilter(
        choices=[('all', 'All')] + list(JOB_TYPE_CHOICES),
        empty_label="Job Position",
        method="filter_all"
    )

    food_type = django_filters.ChoiceFilter(
        choices=[('all', 'All')] + list(FOOD_TYPE_CHOICES),
        empty_label="Cuisine Type",
        method="filter_all"
    )

    # start_date = django_filters.DateFilter(
    #     field_name='date',
    #     lookup_expr='gte',
    #     label="Start Date"
    # )
    #
    # end_date = django_filters.DateFilter(
    #     field_name='date',
    #     lookup_expr='lte',
    #     label="End Date"
    # )

    class Meta:
        model = Post
        fields = ["restaurant_name", "address", "tips_situation", "job_type", "food_type"]

    def filter_all(self, queryset, name, value):
        if value == 'all':
            return queryset
        elif name == "tips_situation":
            return queryset.filter(tips_situation=value)
        elif name == "food_type":
            return queryset.filter(food_type=value)
        elif name == "job_type":
            return queryset.filter(job_type=value)
