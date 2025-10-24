# gpt/urls.py
from django.urls import path
from .views import LocalAPIView

urlpatterns = [
    path("local/", LocalAPIView.as_view(), name="local-api"),
]
