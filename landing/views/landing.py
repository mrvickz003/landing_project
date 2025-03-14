from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
import json

def home_view(request):
    return render(request, "home.html")  # Render the home template

