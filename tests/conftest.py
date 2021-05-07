import pytest
from client import GraphqlClient, GraphqlFileClient


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def file_client():
    return GraphqlFileClient("/graphql")


@pytest.fixture
def client():
    return GraphqlClient("/graphql")
