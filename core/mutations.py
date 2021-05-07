from typing import Any, TypedDict

import graphene
from django.http.request import HttpRequest
from graphql.execution.executor import ResolveInfo


class AppResolverInfo(ResolveInfo):
    context: HttpRequest


class BaseMutation(graphene.relay.ClientIDMutation):
    class Meta:
        abstract = True

    success = graphene.Boolean()

    Input = None

    @classmethod
    def mutate_and_get_payload(
        cls, root, info: AppResolverInfo, **data: Any
    ) -> "BaseMutation":
        ...
