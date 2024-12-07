from rest_framework import serializers


class ForcastGeneratorSerializerRequest(serializers.Serializer):
    STYLE_CHOISES = [
        ('B', 'Tabloid style'),
        ('F', 'factual'),
    ]
    LANGUAGE_CHOICES = [
        ('SK', 'Slovak'),
        ('ENG', 'English'),
    ]

    location = serializers.CharField(max_length=100)
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    style = serializers.ChoiceField(choices=STYLE_CHOISES)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES)


class ForcastGeneratorSerializerResponse(serializers.Serializer):
    headline = serializers.CharField(max_length=255)
    perex = serializers.CharField(max_length=255)
    body = serializers.CharField(max_length=255)


class HistorySerializerRequest(serializers.Serializer):
    location = serializers.CharField(max_length=100)
    date_from = serializers.DateField()
    date_to = serializers.DateField()


class HistorySerializerResponse(serializers.Serializer):
    location = serializers.CharField(max_length=100)
    temperature = serializers.IntegerField()
    date = serializers.DateField()
