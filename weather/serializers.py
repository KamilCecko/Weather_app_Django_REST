from rest_framework import serializers
from .models import WeatherHistory


class TextSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=20)
    date = serializers.CharField(max_length=40)
    STYLE_CHOISES = [
        ('B', 'Tabloid style'),
        ('F', 'factual'),
    ]
    LANGUAGE_CHOICES = [
        ('SK', 'Slovak'),
        ('ENG', 'English'),
    ]
    style = serializers.ChoiceField(choices=STYLE_CHOISES)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES)

class HistorySerializerRequest(serializers.Serializer):
    location = serializers.CharField(max_length=100)
    date_from = serializers.DateField()
    date_to = serializers.DateField()


class HistorySerializerResponse(serializers.Serializer):
    location = serializers.CharField(max_length=100)
    temperature = serializers.IntegerField()
    date = serializers.DateField()

# Generate weather report for today to monday for Bratislava in style factual and in language .Slovak
#             Generated Response should be in Json named weather_report  with keys:json_response and text_response.
#             in json_response i want day as key in format DDMMYYYY and temperature in °C for that day as a value.
#             in text_response i want generate text describing weater . the text should have a headline of up to 10 words,
#              perex up to 25 words and a body of at least 50 words
#             '''
# {
#     "location": "kosice",
#     "date": "dnes",
#     "style": "F",
#     "language": "SK"
# }