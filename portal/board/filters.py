from django_filters import FilterSet
from django_filters.filters import CharFilter, ChoiceFilter, DateTimeFilter
from .models import Ad, Category


class AdFilter(FilterSet):
    category_list = [(rec['id'], rec['name']) for rec in
                     Category.objects.all().values()]

    creation_time = DateTimeFilter(label='Дата создания после',
                                   field_name='creation_time',
                                   lookup_expr='gt')
    category_id = ChoiceFilter(field_name='category_id',
                               label='Категория',
                               choices=category_list,
                               lookup_expr='exact')
    header = CharFilter(label='Заголовок содержит',
                        field_name='header',
                        lookup_expr='icontains')
    ad = CharFilter(label='Объявление содержит',
                    field_name='ad',
                    lookup_expr='icontains')

    class Meta:
        model = Ad
        fields = ['creation_time', 'category_id', 'header', 'ad']
