# Weather Django API

## Project Overview

The task of this project is to design and implement a backend API for an application that provides weather forecasts and presents them in different formats. The application must allow users to get current weather forecasts and view historical weather data for selected locations.

### Project Goals

1. **Text Generation for Weather Forecasts**:
   - A key feature of the application is the ability to generate text articles based on the weather forecast.
   - These articles will interpret the weather forecast in a readable format and will include a headline, perex, and body of the article.
   - Users can choose between two styles: factual or tabloid.
   - Users can choose between two language: Slovak or English.
   - **ChatGPT** is integrated to generate both weather forecasts and articles based on input from the user.

2. **Historical Data Access**:
   - The application allows users to view historical weather data for selected locations.
   - Users can query past weather forecasts based on the location and date range.

3. **Deployment**:
   - The application is deployed on the **AWS** cloud platform. The application is deployed on the AWS cloud platform .The platform is accessible at the following URL: http://3.126.55.96/swagger.

### API Implementation

- **Django REST Framework (DRF)** is used to create the robust backend API for weather forecasts and historical data.
- **drf-yasg** is used to generate Swagger documentation for the API.
- **OpenAI ChatGPT** is integrated to generate both weather forecasts and articles based on user input, removing the need for an external weather forecast API.

### API Endpoints

#### 1. Generate Weather Forecast
- **Endpoint**: `/weather/`
- **Method**: `POST`
- **Description**: Generates a weather forecast based on the given parameters (location, date range, style, language).



**Request**:
```json
{
  "location": "Košice",
  "date_from": "2024-10-16",
  "date_to": "2024-10-18",
  "style": "B",
  "language":"SK"
}
```
*style: Can be 'B' or 'F'. 'B' is for Tabloid style, while 'F' is for Factual style.*

*language: Can be 'SK' or 'ENG'. 'SK' is for the Slovak language, while 'ENG' is for the English language.*


**Response**:
```json
{
  "headline": "Weather in Košice from 16.10. to 18.10.",
  "perex": "Temperatures will range from 13°C to 17°C, with cloudy skies and possible rain.",
  "body": "The sky over Košice will be full of surprises! On 14.10. we expect 15°C, then 17°C on 15.10., and finally 13°C on 16.10. With clouds and a chance of rain, don't forget your umbrella!"
}
```
### Historical Weather Data

- **Endpoint**: /weather/history/
- **Method**: POST
- **Description**: Retrieves historical weather data for a given location and date range.

**Request**:
```json
{
  "location": "Košice",
  "date_from": "2024-10-14",
  "date_to": "2024-10-16"
}
```

**Response**:
```json
[
  {
    "location": "Košice",
    "temperature": 15,
    "date": "2024-10-17"
  },
  {
    "location": "Košice",
    "temperature": 17,
    "date": "2024-10-15"
  },
  {
    "location": "Košice",
    "temperature": 13,
    "date": "2024-10-16"
  }
]
```
### API Documentation

**Endpoint**: /swagger/  
- **Method**: GET  
- **Description**: Access the Swagger UI to explore and interact with the API endpoints. This interface provides an interactive documentation, allowing you to test the API requests and view the responses directly.

  
