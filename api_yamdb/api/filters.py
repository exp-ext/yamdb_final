from django_filters import CharFilter, FilterSet, NumberFilter
from reviews.models import Title


class TitleFilterSet(FilterSet):
    """Фильтр произведений по 4-м полям."""
    name = CharFilter(field_name='name', lookup_expr='icontains')
    category = CharFilter(field_name='category__slug', lookup_expr='icontains')
    genre = CharFilter(field_name='genre__slug', lookup_expr='icontains')
    year = NumberFilter(field_name='year', lookup_expr='exact')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'year', 'name')
