from typing import cast

from articles.mutations.article_mutations import ArticleMutations
from articles.mutations.comment_mutations import CommentsMutations
from articles.queries import ArticleQuery
from graphene import Field, ObjectType, Schema
from graphene_django.debug import DjangoDebug
from users.mutations import UsersMutations
from users.queries import UsersQuery


class AppQuery(UsersQuery, ArticleQuery):
    """root query"""

    debug = Field(DjangoDebug, name="_debug")


class AppMutation(UsersMutations, ArticleMutations, CommentsMutations):
    """root mutation"""


schema = Schema(query=cast(ObjectType, AppQuery), mutation=AppMutation)
