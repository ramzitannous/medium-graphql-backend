from core.mutations import AppResolverInfo
from graphene import ID, Boolean, ObjectType, String, relay
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from users.models import Following, User

####################################
#    Object Types
####################################


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        exclude = ("password",)
        interfaces = (relay.Node,)


class UserDetailsType:
    email = String(required=True)
    username = String(required=True)
    bio = String()


class Profile(UserDetailsType, ObjectType):
    image = String()
    following = Boolean(required=True)
    id = ID()

    @staticmethod
    def resolve_following(root: User, info: AppResolverInfo) -> bool:
        follower = info.context.user
        following_exists = Following.objects.is_following(follower, root)
        return following_exists


####################################
#    Input Types
####################################


class UserCreateInputType(UserDetailsType):
    password = String(required=True)
    confirm_password = String(required=True)
    image = Upload()


class UserUpdateInputType:
    email = String()
    username = String()
    bio = String()


class ProfileFollowInput:
    username = String(required=True)
