from typing import Optional

from django.conf import settings
from django.http.response import HttpResponse
from django.test.client import Client
from graphene_django.utils.testing import graphql_query
from graphene_file_upload.django.testing import file_graphql_query
from graphql_jwt.shortcuts import get_token
from users.models import User


class GraphqlFileClient:
    def __init__(self, graphql_url: str):
        self._url = graphql_url
        self._client = Client()

    def query(
        self,
        query: str,
        op_name: Optional[str] = None,
        input_data: Optional[dict] = None,
        variables: Optional[dict] = None,
        headers: Optional[dict] = None,
        files: Optional[dict] = None,
    ) -> HttpResponse:
        response = file_graphql_query(
            query,
            op_name,
            input_data,
            variables,
            headers,
            files,
            self._client,
            self._url,
        )
        return response


class GraphqlClient:
    def __init__(self, graphql_url: str):
        self._url = graphql_url
        self._client = Client()

    def query(
        self,
        query: str,
        op_name: Optional[str] = None,
        input_data: Optional[dict] = None,
        variables: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> HttpResponse:
        response = graphql_query(
            query, op_name, input_data, variables, headers, self._client, self._url
        )
        return response

    def authenticated_query(
        self,
        user: User,
        query: str,
        op_name: Optional[str] = None,
        input_data: Optional[dict] = None,
        variables: Optional[dict] = None,
    ) -> HttpResponse:
        token = get_token(user)
        headers = {settings.GRAPHQL_JWT["JWT_AUTH_HEADER_NAME"]: f"JWT {token}"}
        return self.query(query, op_name, input_data, variables, headers)
