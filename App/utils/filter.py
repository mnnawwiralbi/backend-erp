import django_filters
from App.models import Article


class ArticleFilter(django_filters.FilterSet):
    # Menggunakan icontains untuk pencarian IP
    ip = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Article
        fields = ['title', 'content']
