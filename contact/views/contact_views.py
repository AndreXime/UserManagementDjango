from django.shortcuts import render
from ..forms import ClientForm

def index(request):
    return render(request,'contact/index.html')

def login(request):
    return render(request,'contact/login.html')
