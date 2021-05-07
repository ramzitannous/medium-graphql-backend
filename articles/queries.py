import graphene_django_optimizer as gql_optimizer
from articles.filters import ArticleFilterSet
from articles.models import Article
from articles.types import ArticleNode
from core.mutations import AppResolverInfo
from django.db.models.query import QuerySet
from graphene import Field, ObjectType, String
from graphene_django.filter import DjangoFilterConnectionField


class ArticleQuery(ObjectType):
    articles = DjangoFilterConnectionField(
        ArticleNode, filterset_class=ArticleFilterSet
    )
    get_article = Field(ArticleNode, slug=String(required=True))

    @staticmethod
    def resolve_articles(root, info: AppResolverInfo, **fields) -> QuerySet[Article]:
        return gql_optimizer.query(Article.objects.all(), info, disable_abort_only=True)

    @staticmethod
    def resolve_get_article(root, info: AppResolverInfo, **fields) -> QuerySet[Article]:
        optimized_query = gql_optimizer.query(
            Article.objects.filter(slug=fields.get("slug")),
            info,
            disable_abort_only=True,
        )
        return optimized_query.first()
