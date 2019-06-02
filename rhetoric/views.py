from django.shortcuts import render
from . import apis
import rhetoric.apis.faceexpressionmodel.faceexpressionmodel as facescoremodel

# Create your views here.

def home(request):
  return render(request, 'rhetoric/home.html')

def upload(request):
  return render(request, 'rhetoric/upload.html')

def review(request):
  result = facescoremodel.main(request)
  return result