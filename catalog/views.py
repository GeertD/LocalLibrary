from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Index page')

def say_hello(request):
    return HttpResponse('Hello World')
