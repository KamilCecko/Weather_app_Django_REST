from django.urls import path
from .views import text_processing, weather_history

urlpatterns = [
    path("", text_processing, name="text_processing"),
    path("history/", weather_history, name="weather_history")
    ]
