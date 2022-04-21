import os
from django.apps import apps
from django.conf import settings
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
apps.populate(settings.INSTALLED_APPS)


from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.middleware.cors import CORSMiddleware

from api.endpoints import api_router

from importlib.util import find_spec
from fastapi.staticfiles import StaticFiles

from main.settings import STATIC_ROOT


def get_application() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

    #print(STATIC_ROOT)

    app.mount('/static',
        StaticFiles(
             directory=os.path.normpath(
                  os.path.join(STATIC_ROOT, '..', 'static')
             )
       ),
       name='static',
    )

    # app.mount('/static',
    #     StaticFiles(
    #          directory=os.path.normpath(
    #               os.path.join(find_spec('django.contrib.admin').origin, '..', 'static')
    #          )
    #    ),
    #    name='static',
    # )
    #app.mount("/public/static", StaticFiles(directory="public/static"), name="static")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix="/api")
    app.mount("/", WSGIMiddleware(get_wsgi_application()))

    return app


app = get_application()
