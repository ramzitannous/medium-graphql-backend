import graphene
import graphene_django_optimizer as gql_optimizer
from core.mutations import AppResolverInfo
from django.db.models.query import QuerySet
from graphene import ObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from users.models import User
from users.types import Profile, UserNode


class UsersQuery(ObjectType):
    current_user = graphene.Field(UserNode)
    get_profile = graphene.Field(Profile, username=graphene.String(required=True))

    @staticmethod
    def resolve_current_user(root, info: AppResolverInfo, **kwargs) -> QuerySet[User]:
        if not info.context.user or not info.context.user.is_authenticated:
            raise GraphQLError("No User Logged in")
        optimized_query = gql_optimizer.query(
            User.objects.filter(id=info.context.user.id), info
        )
        return optimized_query.first()

    @staticmethod
    @login_required
    def resolve_get_profile(
        root, info: AppResolverInfo, username: str
    ) -> QuerySet[User]:
        optimized_query = gql_optimizer.query(User.objects.get(username=username), info)
        return optimized_query
