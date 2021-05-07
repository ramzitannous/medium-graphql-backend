from typing import Any

from graphene import Field, ObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from articles.models import Article, FavoriteArticles
from articles.types import (
    ArticleCreateInputType,
    ArticleDeleteInputType,
    ArticleNode,
    ArticleUpdateInputType,
    FavoriteInputType,
)
from core.mutations import AppResolverInfo, BaseMutation

####################################
#    Articles Mutations
####################################


class CreateArticleMutation(BaseMutation):
    article = Field(ArticleNode)

    Input = ArticleCreateInputType

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls, root, info: AppResolverInfo, **data: Any
    ) -> "BaseMutation":
        article = Article(**data, author=info.context.user)
        article.save()
        return CreateArticleMutation(success=True, article=article)


class DeleteArticleMutation(BaseMutation):
    Input = ArticleDeleteInputType

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls, root, info: AppResolverInfo, **data: Any
    ) -> "BaseMutation":
        article = Article.objects.select_related("author").get(slug=data.get("slug"))
        if not article.author == info.context.user:
            raise GraphQLError("only article owner can delete it")
        article.delete()
        return DeleteArticleMutation(success=True)


class UpdateArticleMutation(BaseMutation):
    Input = ArticleUpdateInputType

    article = Field(ArticleNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls, root, info: AppResolverInfo, **data: Any
    ) -> "BaseMutation":
        article = Article.objects.select_related("author").get(slug=data.pop("slug"))
        if not article.author == info.context.user:
            raise GraphQLError("only article owner can edit it")
        for name, value in data:
            setattr(article, name, value)
        article.save()
        return UpdateArticleMutation(success=True, article=article)


class FavoriteArticleMutation(BaseMutation):
    Input = FavoriteInputType

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls, root, info: AppResolverInfo, article_slug: str
    ) -> "FavoriteArticleMutation":
        article = Article.objects.get(slug=article_slug)
        favorite = FavoriteArticles(user=info.context.user, article=article)
        favorite.save()
        return FavoriteArticleMutation(success=True)


class UnFavoriteArticleMutation(BaseMutation):
    Input = FavoriteInputType

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls, root, info: AppResolverInfo, article_slug: str
    ) -> "UnFavoriteArticleMutation":
        favorite = FavoriteArticles.objects.get(
            article__slug=article_slug, user=info.context.user
        )
        favorite.delete()
        return UnFavoriteArticleMutation(success=True)


class ArticleMutations(ObjectType):
    create_article = CreateArticleMutation.Field(description="create a new article")
    delete_article = DeleteArticleMutation.Field(
        description="delete an article by slugs"
    )
    update_article = UpdateArticleMutation.Field(
        description="update an article by slug"
    )
    favorite_article = FavoriteArticleMutation.Field(
        description="favorite an article by its slug"
    )
    unfavorite_article = UnFavoriteArticleMutation.Field(
        description="remove article from favorite by its slug"
    )
