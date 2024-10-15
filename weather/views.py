from datetime import datetime
from rest_framework.decorators import api_view
from .serializers import TextSerializer, HistorySerializerRequest, HistorySerializerResponse
from rest_framework.response import Response
from rest_framework import status
from .models import WeatherHistory
import requests
import json



@api_view(['POST'])
def text_processing(request):
    serializer_textu = TextSerializer(data=request.data)
    if serializer_textu.is_valid():
        location = serializer_textu.validated_data['location']
        date = serializer_textu.validated_data['date']
        style = serializer_textu.validated_data['style']
        if style == 'B':
            style = 'Tabloid style'
        else:
            style = 'factual'
        language = serializer_textu.validated_data['language']
        if language == 'SK':
            language = 'Slovak'
        else:
            language = 'English'
        # prompt = f''' Generate weather report for {date} for {location} in style {style} and in language {language_choises}.
        # Generated Response should be in Json with keys:json_response and text_response.
        # in json_response i want day as key in format YYYY-MM-DD and temperature in °C for that day as a value.
        # in text_response i want generate text describing weater . the text should have a headline of up to 10 words,
        #  perex up to 25 words and a body of at least 50 words
        # '''
        # headers = {
        #        "Content-Type": "application/json",
        #        "Authorization": f"Bearer {REMOVED}"
        #    }
        # data = {
        #        "model": "gpt-3.5-turbo",
        #        "messages": [{"role": "user", "content": prompt}],
        #        "max_tokens": 500
        #    }
        # response = requests.post(URL, headers=headers, json=data)
        # if response.status_code == 200:
        #     generated_text = response.json()['choices'][0]['message']['content']['text_response']
            # generated_json = response.json()['choices'][0]['message']['content']['json_response']
        generated_text = {
        "headline": "Bratislava: Počasie na týždeň vpred!",
        "perex": "Zistite, čo nás čaká v Bratislave tento týždeň.",
        "body": "Tento týždeň sa v Bratislave môžeme tešiť na rozmanité počasie. Od piatku 11. októbra budú teploty kolísať medzi 13 °C a 16 °C. Očakáva sa, že najteplejšie dni budú v piatok a nedeľu, kedy teploty dosiahnu príjemných 16 °C. Počas víkendu však môže pršať, takže nezabudnite na dáždnik! Na začiatku budúceho týždňa sa ochladí, pričom v pondelok očakávame len 13 °C. S prichádzajúcim chladom bude nutné si obliecť teplejšie vrstvy. Tento týždeň sa budú striedať oblačné a slnečné dni, takže si vychutnajte každú chvíľu vonku!"
            }
        generated_json = {
                    "2024-10-11": 16,
                    "2024-10-12": 14,
                    "2024-10-13": 15,
                    "2024-10-14": 13,
                    "2024-10-15": 15,
                    "2024-10-16": 14,
                    "2024-10-17": 14,
                }
        # history_dict = json.loads(generated_json)
        object_to_create = []
        for date, temperature in generated_json.items():
            obj = WeatherHistory(
                location=location,
                temperature=temperature,
                date=date,
            )
            object_to_create.append(obj)
        if object_to_create:
            WeatherHistory.objects.bulk_create(object_to_create)
        return Response(generated_text, status=status.HTTP_200_OK)
    return Response(TextSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def weather_history(request):
    if request.method == 'GET':
        all_weather = WeatherHistory.objects.all()
        serializer = HistorySerializerResponse(all_weather, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        serializer = HistorySerializerRequest(data=request.data)
        if serializer.is_valid():
            location = serializer.validated_data.get('location')
            date_from = serializer.validated_data.get('date_from')
            date_to = serializer.validated_data.get('date_to')
            filtered = WeatherHistory.objects.filter(
                location__iexact=location,
                date__range=[date_from, date_to],
            )
            serializer = HistorySerializerResponse(filtered, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


# Successfully installed python-decouple-3.8
# Domena
# WARNING! Your password will be stored unencrypted in /root/.docker/config.json.