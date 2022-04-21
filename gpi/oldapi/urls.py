from django.urls import path
from rest_framework.schemas import get_schema_view

from rest_framework.documentation import include_docs_urls

from . import views

urlpatterns = [
    path("", views.root, name="root"),
    path("docs/", include_docs_urls(title="Glass Plate Inventory API")),

    # custom API
    path('archive/', views.archive, name="archive"),
    path('<str:archive>/', views.PlateArchive, name="PlateArchive"),
    path('<str:archive>/<str:identifier>/', views.GlassPlate, name="GlassPlate"),
]