from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<archive_id>/", views.archive, name="archive"),
    path("<archive_id>/<str:plate_id>/", views.plate, name="plate"),
]
