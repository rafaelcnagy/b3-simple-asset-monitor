from django.shortcuts import render
from django.http import HttpResponse
from .api import API

def update_data(request):
    API()
    return HttpResponse("Updated data")

