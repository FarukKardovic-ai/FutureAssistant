import logging
import os
import math
from newsapi import NewsApiClient

import requests

def get_weather(city: str):
    if not city:
        return "City is not provided"
    
    # First, geocode the city name to get latitude and longitude
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1}
    ).json()
    if "results" not in geo or not geo["results"]:
        return f"City '{city}' not found"

    loc = geo["results"][0]
    lat, lon = loc["latitude"], loc["longitude"]

    # Then, fetch current weather
    weather = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        }
    ).json()

    cw = weather.get("current_weather")
    if not cw:
        return "Could not fetch current weather"

    desc = f"{cw['temperature']}°C, wind {cw['windspeed']} m/s, code {cw['weathercode']}"
    return f"Current weather in {city}: {desc}"

# Example
print(get_weather("Milan"))

def get_news():
    api_key = '21937fe1ec884aa0939c3fcdf0c8256d'
    newsapi = NewsApiClient(api_key=api_key)

    try:
        # Fetch top headlines
        top_headlines = newsapi.get_top_headlines(language='en', country='us')

        # Extract titles from the articles
        headlines = [article['title'] for article in top_headlines['articles']]

        # Join the titles into a single string
        return 'Latest News Headlines:\n' + '\n'.join(headlines)

    except Exception as e:
        return f"An error occurred while fetching news: {e}"

# Function to perform basic arithmetic calculations
def calculate(operation, num1, num2):
    if operation == 'add':
        return num1 + num2
    elif operation == 'subtract':
        return num1 - num2
    elif operation == 'multiply':
        return num1 * num2
    elif operation == 'divide':
        if num2 == 0:
            return "Cannot divide by zero"
        return num1 / num2
    else:
        return "Unknown operation"

def calculate_bmi(weight_kg: float, height_cm: float, age: int = None) -> str:
    if weight_kg <= 0 or height_cm <= 0:
        return "Invalid weight or height"

    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    
    # Classification based on WHO standards
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 24.9:
        category = "Normal weight"
    elif bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obese"

    result = f"Your BMI is {bmi:.1f} ({category})."
    if age is not None:
        result += f" Age provided: {age}."

    return result

# Example usage
print(calculate_bmi(weight_kg=70, height_cm=175, age=30))
