from django.shortcuts import render
import requests

def home(request):
    api_url = "http://127.0.0.1:8000/api/parking/slots/"

    response = requests.get(api_url)
    slots = response.json()

    return render(request, "frontend/index.html", {"slots": slots})
