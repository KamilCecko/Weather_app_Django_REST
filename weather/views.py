import os
from rest_framework import status
from .models import WeatherHistory
import requests
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import ForcastGeneratorSerializerRequest, HistorySerializerRequest, HistorySerializerResponse, ForcastGeneratorSerializerResponse


URL = "https://api.openai.com/v1/chat/completions"


@swagger_auto_schema(
    method='post',
    request_body=ForcastGeneratorSerializerRequest,
    responses={
        200: ForcastGeneratorSerializerResponse,
        400: 'Bad Request',
        500: 'Internal Server Error'
    },
)
@api_view(['POST'])
def text_processing(request):
    serializer = ForcastGeneratorSerializerRequest(data=request.data)
    if serializer.is_valid():
        location = serializer.validated_data['location']
        date_from = serializer.validated_data['date_from']
        date_to = serializer.validated_data['date_to']
        openai_api_key = serializer.validated_data['openai_api_key']
        style = 'Tabloid' if serializer.validated_data['style'] == 'B' else 'factual'
        language = 'Slovak' if serializer.validated_data['language'] == 'SK' else 'English'

        generated_text = {}
        generated_json = {}

        prompt = f''' Generate weather report for date between {date_from} and {date_to} for {location} in {style} style and in {language} language.
        Generated Response should be in Json with keys:json_response and text_response.
        in json_response i want day as key in format YYYY-MM-DD and temperature in celzius for that day as a value.
        in text_response i want generate text describing weater. the text_response should have key headline with string value max 50 character,
        key perex with string value max 100 characters and a key body with string value max 200 characters
        '''
        headers = {
               'Content-Type': 'application/json',
               'Authorization': f'Bearer {openai_api_key}'
           }
        data = {
               'model': 'gpt-3.5-turbo',
               'messages': [{'role': 'user', 'content': prompt}],
               'max_tokens': 500
           }
        response = requests.post(URL, headers=headers, json=data)
        if response.status_code == 200:
            try:
                json_response = json.loads(response.json()['choices'][0]['message']['content'])

                generated_text = json_response.get('text_response')
                generated_json = json_response.get('json_response')

            except KeyError as error:
                return Response(data='wrong ChatGTP response', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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
        response_serializer = ForcastGeneratorSerializerResponse(data=generated_text)
        if response_serializer.is_valid():
            return Response(response_serializer.data, status=status.HTTP_200_OK)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=HistorySerializerRequest,
    responses={
        200: HistorySerializerResponse,
        400: 'Bad Request',
        404: 'Not Found',
        500: 'Internal Server Error'
    },
)
@api_view(['POST'])
def weather_history(request):
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
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
