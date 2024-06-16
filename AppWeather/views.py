from django.shortcuts import render

# Create your views here.
import urllib.request
import json
import requests

def home(request):
    context = {}
    if request.method == "POST":
        city = request.POST.get('city')
        api_key = '8d5f8cb66002cd42c4a55c615f333071'  # Replace with your OpenWeatherMap API key
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}'

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            weather_data = response.json()

            if weather_data['cod'] == '200':
                forecast_list = []
                for i in range(0, len(weather_data['list']), 8):  # 8 intervals per day (3 hours each)
                    day_data = weather_data['list'][i]
                    forecast = {
                        'date': day_data['dt_txt'].split(' ')[0],
                        'description': day_data['weather'][0]['description'],
                        'temperature': day_data['main']['temp'],
                        'pressure': day_data['main']['pressure'],
                        'humidity': day_data['main']['humidity'],
                        'icon': day_data['weather'][0]['icon']
                    }
                    forecast_list.append(forecast)

                context = {
                    'city': weather_data['city']['name'],
                    'forecast_list': forecast_list,
                }
            else:
                context = {'error': 'City not found.'}

        except requests.exceptions.HTTPError as http_err:
            context = {'error': f'HTTP error occurred: {http_err}'}
        except requests.exceptions.ConnectionError as conn_err:
            context = {'error': f'Connection error occurred: {conn_err}'}
        except requests.exceptions.Timeout as timeout_err:
            context = {'error': f'Timeout error occurred: {timeout_err}'}
        except requests.exceptions.RequestException as req_err:
            context = {'error': f'An error occurred: {req_err}'}

    return render(request, 'main/index.html', context)