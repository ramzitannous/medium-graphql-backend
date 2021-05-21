
 
# [Graphql RealWorld Example App] 


> ### [Graphene-Django](https://docs.graphene-python.org/projects/django/en/latest/#graphene-django) codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld) spec and API.

A Graphql server implementation using [Graphene-Django](https://docs.graphene-python.org/projects/django/en/latest/#graphene-django)

<img src="https://raw.githubusercontent.com/ramzitannous/medium-graphql-backend/master/logo.png" height="200" width="400"/>

This codebase was created to demonstrate a fully fledged fullstack application built with Django including CRUD operations, authentication, routing, pagination, and more.

For more information on how to this works with other frontends/backends, head over to the [RealWorld](https://github.com/gothinkster/realworld) repo.
## Screenshots

<img src="https://raw.githubusercontent.com/ramzitannous/medium-graphql-backend/master/example_images/article_query.png" width="800" height="400"/>

<img src="https://raw.githubusercontent.com/ramzitannous/medium-graphql-backend/master/example_images/add_article.png" width="800" height="400"/>

<img src="https://raw.githubusercontent.com/ramzitannous/medium-graphql-backend/master/example_images/add_comment.png" width="800" height="400"/>

<img src="https://raw.githubusercontent.com/ramzitannous/medium-graphql-backend/master/example_images/get_profile.png" width="800" height="400"/>

<img src="https://raw.githubusercontent.com/ramzitannous/medium-graphql-backend/master/example_images/current_user.png" width="800" height="400"/>

# How it works
A Graphql Implementation using facebook relay specs

Full graphql schema can be found at [`schema.graphql`](https://github.com/ramzitannous/medium-graphql-backend/blob/master/schema.graphql)

**Folder Structure:**
1) `core`: contains all core functionalites ex (BaseModel, BaseMutation)
2) `users` contains user related mutation, models, types, queries
3) `articles` contains all article related models, mutation, types, queries
4) `tests` all test related stuff
5) `medium` contains all django urls, settings, and others.

# Getting started

1) Install dependancies
`poetry install`

2) create `.env` file with this content
`DEBUG=True ` 
`SECRET_KEY=test-secret-key`
 `DATABASE_URL=postgresql://postgres:password@localhost:5432/medium`
 3) run migration
 `poetry run python manage.py migrate`
4) run server
`poetry  run python manage.py runserver 8000`
5) open graphql playground using http://localhost:8000/playground
6) to connect to it via API use http://localhost:8000/graphql


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
****
