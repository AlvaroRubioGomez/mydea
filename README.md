# MyDea

This is MyDea, a solution to the django backend technical test from Z1 Digital presented by Alvaro Rubio Gomez

<a href="https://github.com/pydanny/cookiecutter-django/"">
<img src="https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter"     
     alt="Built with Cookiecutter Django" /></a>

<a href="https://github.com/ambv/black">
<img src="https://img.shields.io/badge/code%20style-black-000000.svg"    
     alt="Black code style" /></a>

License: **MIT**

## Requirements
* [Docker engine](https://docs.docker.com/engine/)
* [Docker compose](https://docs.docker.com/compose/)

## Run MyDea

1. Build docker

It is highly recommended to create a python [virtual environment](https://docs.python.org/3/library/venv.html) to avoid dependencies conflicts with other projects.

After you have cloned the mydea repository, build the docker by running inside the project root folder:

```
export COMPOSE_FILE=local.yml
docker-compose build
```
And wait until it is finished.

2. Make and run migrations

After the docker build has finished, run the migrations to reflect the models inside the database by running:

```
docker-compose run --rm django python manage.py makemigrations
docker-compose run --rm django python manage.py migrate

```

3. Run the project

Up the server by running:
```
docker-compose up
```

## Try MyDea

After the project is up, you can consult and perform the graphql queries and mutations in `http://localhost:8000/graphql`

Alternatively, you can use postman and import the files located in the postman folder, which contains examples of all the queries and mutations of MyDea.
 
To access the admin site at `http://localhost:8000/admin` you need to create a superuser first by running:
```
docker-compose run --rm django python manage.py createsuperuser
```
In the admin site you can consult, add and delete instances to your database.

## Testing

MyDea has been developed following the TDD methodology. 
Each app folder contains a `tests` where you can consult all the unit tests performed.

Run all the unit tests by running:
```
docker-compose run --rm django pytest -v
```







