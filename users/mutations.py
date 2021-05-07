import uuid
from typing import Any

import graphene
import graphql_jwt
from core.mutations import AppResolverInfo, BaseMutation
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from users.models import Following, User
from users.types import (ProfileFollowInput, UserCreateInputType, UserNode,
                         UserUpdateInputType)

####################################
#    Users Mutations
####################################


class CreateUserMutation(BaseMutation):
    Input = UserCreateInputType

    user = graphene.Field(UserNode, required=True)

    @classmethod
    def mutate_and_get_payload(
        cls, root, info: AppResolverInfo, **data
    ) -> "CreateUserMutation":
        password = data.get("password")
        confirm_password = data.pop("confirm_password")
        if not password == confirm_password:
            raise GraphQLError("password and confirm_password must match")

        user = User.objects.create_user(**data)
        image = info.context.FILES.get("image")
        if image is not None:
            user.image.save(str(uuid.uuid4()), image)

        return CreateUserMutation(success=True, user=user)


class UpdateUserMutation(BaseMutation):
    Input = UserUpdateInputType

    user = graphene.Field(UserNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls, root, info: AppResolverInfo, **data: Any
    ) -> "UpdateUserMutation":
        current_user = info.context.user
        for key, value in data.items():
            setattr(current_user, key, value)
            current_user.save()
        return UpdateUserMutation(user=current_user, success=True)


####################################
#    Profile Mutations
####################################


class FollowProfileMutation(BaseMutation):
    Input = ProfileFollowInput

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls, root, info: AppResolverInfo, **data: Any
    ) -> "BaseMutation":

        current_user = info.context.user
        username: str = data.get("username")
        profile = User.objects.get(username=username)
        result = Following.objects.follow(current_user, profile)
        if result:
            return FollowProfileMutation(success=True)
        return FollowProfileMutation(success=False)


class UnFollowProfileMutation(BaseMutation):
    Input = ProfileFollowInput

    @classmethod
    def mutate_and_get_payload(
        cls, root, info: AppResolverInfo, **data: Any
    ) -> "UnFollowProfileMutation":
        username: str = data.get("username")
        followed = User.objects.get(username=username)
        following = Following.objects.unfollow(info.context.user, followed)
        if following:
            return UnFollowProfileMutation(success=True)
        return UnFollowProfileMutation(success=False)


####################################
#    Users Authentication
####################################


class UserLoginMutation(graphql_jwt.relay.JSONWebTokenMutation):
    user = graphene.Field(UserNode)

    @classmethod
    def resolve(cls, _, info, **kwargs):
        return cls(user=info.context.user)


class UsersMutations(graphene.ObjectType):
    create_user = CreateUserMutation.Field(description="create a new user")
    update_user = UpdateUserMutation.Field(
        description="update the current logged in user"
    )

    login_user = UserLoginMutation.Field()
    verify_token = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()

    follow_profile = FollowProfileMutation.Field(description="follow a profile")
    unfollow_profile = UnFollowProfileMutation.Field(description="unfollow a profile")
