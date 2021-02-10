
from pathlib import Path

from django.urls import path

from . import views
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


urlpatterns = [
    path("", views.index, name="index"),
]
