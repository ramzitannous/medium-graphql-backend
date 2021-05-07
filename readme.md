# [Graphql RealWorld Example App]

> ### [Graphene-Django](https://docs.graphene-python.org/projects/django/en/latest/#graphene-django) codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld) spec and API.

A Graphql server implementation using [Graphene-Django](https://docs.graphene-python.org/projects/django/en/latest/#graphene-django)

This codebase was created to demonstrate a fully fledged fullstack application built with Django including CRUD operations, authentication, routing, pagination, and more.

For more information on how to this works with other frontends/backends, head over to the [RealWorld](https://github.com/gothinkster/realworld) repo.


# How it works

A Graphql Implementation with facebook relay specs

Full graphql schema can be found at `schema.graphql`

# Getting started

1) Install dependancies
`poetry install`

2) create `.env` file with this content
`DEBUG=True ` 
`SECRET_KEY=test-secret-key`
 `DATABASE_URL=postgresql://postgres:password@localhost:5432/medium`
3) run server
`poetry  run python manage.py runserver 8000`
4) open playground using http://localhost:8000/graphql

## Third Party Packages
1) `graphene-django`: Add Graphql to a django server
2) `python-decouple`: manage django settings using .env file
3) `django-graphql-jwt`: Add JWT authentication
4) `graphene-django-optimizer`: Optimize database queries to avoid N+1 problem
5) `graphene-file-upload`: Add mutlipart file upload mutations to graphene

## Testing
some tests were added to `tests` directory, packages used for testing:
1) `pytest`
2) `pytest-django`
3) `factory-boy`
