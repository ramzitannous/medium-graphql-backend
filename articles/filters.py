from articles.models import Article
from django.db.models import QuerySet
from django_filters import CharFilter, FilterSet


class ArticleFilterSet(FilterSet):
    tag = CharFilter(method="filter_tags")
    author_name = CharFilter("author__username")

    class Meta:
        model = Article
        fields = ("slug", "title")

    def filter_tags(
        self, query: QuerySet["Article"], *, value: str
    ) -> QuerySet["Article"]:
        return query.filter(tags__contains=[value])
