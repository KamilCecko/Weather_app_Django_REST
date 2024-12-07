from rest_framework import status
from .models import WeatherHistory
import json
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import ForcastGeneratorSerializerRequest, HistorySerializerRequest, HistorySerializerResponse, ForcastGeneratorSerializerResponse
from rest_framework import generics
from openai import OpenAI

client = OpenAI()


class TextProcessor(generics.CreateAPIView):
    serializer_class = ForcastGeneratorSerializerRequest

    @swagger_auto_schema(
        request_body=ForcastGeneratorSerializerRequest,
        responses={
            200: ForcastGeneratorSerializerResponse,
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
    )
    def post(self, request):
        serializer = ForcastGeneratorSerializerRequest(data=request.data)
        if serializer.is_valid():
            location = serializer.validated_data['location']
            date_from = serializer.validated_data['date_from']
            date_to = serializer.validated_data['date_to']
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

            try:
                completion = client.chat.completions.create(
                    model='gpt-3.5-turbo',
                    messages=[
                        {"role": "system", "content": "You are a weather expert providing accurate forecasts."},
                        {
                            "role": "user",
                            "content": f'''{prompt}'''
                        }
                    ]
                )
            except Exception as e:
                return Response(data=f'Error calling OpenAi API: {str(e)}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            json_response = completion.choices[0].message.content
            json_dict = json.loads(json_response)

            generated_text = json_dict.get('text_response')
            generated_json = json_dict.get('json_response')
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchWeatherHistory(generics.GenericAPIView):
    serializer_class = HistorySerializerRequest

    @swagger_auto_schema(
        query_serializer=HistorySerializerRequest,
        responses={
            200: HistorySerializerResponse,
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
    )
    def get(self, request):
        location = request.query_params.get('location')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        if location and date_from and date_to:
            filtered = WeatherHistory.objects.filter(
                location__iexact=location,
                date__range=[date_from, date_to],
            )
        else:
            return Response({"detail": "No weather history found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = HistorySerializerResponse(filtered, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
