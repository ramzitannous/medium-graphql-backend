from articles.dataloaders import ArticleFavoriteDataLoader
from articles.models import Article, Comment
from core.mutations import AppResolverInfo
from graphene import ID, Boolean, Int, List, Node, String
from graphene_django import DjangoObjectType
from users.types import Profile

####################################
#    Object Types
####################################

article_loader = ArticleFavoriteDataLoader()


class ArticleNode(DjangoObjectType):
    author = Profile()
    favorited = Boolean()
    favorites_count = Int()

    class Meta:
        model = Article
        fields = "__all__"
        interfaces = (Node,)

    @staticmethod
    def resolve_favorited(root: Article, info: AppResolverInfo):
        return article_loader.load((info.context.user, root)).get()["favorited"]

    @staticmethod
    def resolve_favorites_count(root: Article, info: AppResolverInfo):
        return article_loader.load((info.context.user, root)).get()["favorites_count"]


class CommentNode(DjangoObjectType):
    class Meta:
        model = Comment
        exclude = ("article",)
        interfaces = (Node,)


####################################
#    Input Types
####################################


class ArticleCreateInputType:
    title = String(required=True)
    slug = String(requited=True)
    description = String(required=False)
    body = String(required=True)
    tags = List(String)


class ArticleUpdateInputType:
    slug = String(required=True)
    title = String()
    description = String()
    body = String()


class ArticleDeleteInputType:
    slug = String(required=True)


class CommentCreateInputType:
    body = String(required=True)
    article_slug = String(required=True)


class CommentDeleteInputType:
    comment_id = ID(required=True)


class FavoriteInputType:
    article_slug = String(required=True)
