from .views import BasePage
from django.urls import path

urlpatterns = [
   path("", BasePage.as_view(), name="Base")
]
