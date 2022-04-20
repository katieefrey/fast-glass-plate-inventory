## notes
https://www.mongodb.com/developer/quickstart/python-quickstart-fastapi/

https://www.stavros.io/posts/fastapi-with-django/

https://stackoverflow.com/questions/63726203/is-it-possible-to-use-fastapi-with-django

https://github.com/mongodb-developer/mongodb-with-fastapi




http://127.0.0.1:8000/docs

http://127.0.0.1:8000/api/items

https://fastapi.tiangolo.com/#installation
https://fastapi.tiangolo.com/advanced/nosql-databases/


# django-fastapi-example

Another Django + FastAPI example can be found here: https://github.com/jordaneremieff/aeroplane/

This is an experiment to demonstrate one potential way of running FastAPI with Django. It won't be actively maintained. If you're interested in using FastAPI with Django, then you should just use this for inspiration.

## Setup

```
pip install -r requirements.txt
cd django_fastapi/
./manage.py migrate
./manage.py createsuperuser 
```

## Running

```
uvicorn project.asgi:app --debug
```

## Routes

The Django app is available at `/` (e.g. `http://localhost:8000/admin/`

The FastAPI app is is available at `/api` (e.g. `http://localhost:8000/api/items/`
