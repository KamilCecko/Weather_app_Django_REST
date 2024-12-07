from django.urls import path
from .views import TextProcessor, SearchWeatherHistory

urlpatterns = [
    path("", TextProcessor.as_view(), name="text_processing"),
    path("history/", SearchWeatherHistory.as_view(), name="weather_history")
    ]
