from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("fetch_ah_data/", views.fetch_ah_data, name="fetch_ah_data")
]
