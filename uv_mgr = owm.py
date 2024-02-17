import django
from django.urls import path

urlpatterns = [
]
...

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'weather',
]

...
from django.shortcuts import render

def index(request):
    return render(request, 'weather/index.html') #returns the index.html template
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),  #the path for our index view
]
python manage.py runserver
from django.shortcuts import render
import requests

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=YOUR_APP_KEY'

    city = 'Las Vegas'

    city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

    return render(request, 'weather/index.html') #returns the index.html template
...
def index(request):
    ...
    print(city_weather) #temporarily view output

    return render(request, 'weather/index.html') #returns the index.html template
...
def index(request):
    ...
    weather = {
        'city' : city,
        'temperature' : city_weather['main']['temp'],
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon']
    }

    return render(request, 'weather/index.html') #returns the index.html template
...
def index(request):
    ...
    context = {'weather' : weather}

    return render(request, 'weather/index.html', context) #returns the index.html template
from django.db import models

class City(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self): #show the actual city name on the dashboard
        return self.name

    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'cities'
        from django.contrib import admin
from .models import City

admin.site.register(City)
from django.shortcuts import render
import requests
from .models import City
...
def index(request):
    ...
    cities = City.objects.all() #return all the cities in the database

    weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather) #add the data for the current city into our list

    context = {'weather_data' : weather_data}

 return render(request, 'weather/index.html', context) #returns the index.html template
from django.forms import ModelForm, TextInput
from .models import City

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'}),
        } #updates the input class to have the correct Bulma class and placeholder
    ...
from .forms import CityForm

def index(request):
    ...
    form = CityForm()

    weather_data = []
    ...
    context = {'weather_data' : weather_data, 'form' : form}
    ...
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=YOUR_APP_KEY'

    cities = City.objects.all() #return all the cities in the database

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate

    form = CityForm()
    ...
    