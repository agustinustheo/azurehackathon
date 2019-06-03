import json
from . import apis
from django.shortcuts import render
from django.http import HttpResponse
import rhetoric.apis.faceexpressionmodel.faceexpressionmodel as facescoremodel

# Create your views here.

def home(request):
  return render(request, 'rhetoric/home.html')

def upload(request):
  return render(request, 'rhetoric/upload.html')

def review(request):
  face_result = facescoremodel.main(request)

  if face_result["error"]:
    result = "Error: " + face_result["err_msg"]

    return HttpResponse(result)
  else:
    tense = ""
    anger = ""
    micro_tense = ""
    micro_anger = ""
    if face_result["tense_count"] > 0:
      tense = "You are seen as tense in some parts of the video, I detected about " + str(face_result["tense_count"]) + " moments when you seem tense."
    if face_result["anger_count"] > 0:
      anger = "Your seen to be angry in some parts of the video, I counted about " + str(face_result["anger_count"]) + " times you looked angry."
    if face_result["micro_tense_count"] > 0:
      micro_tense = "You still seem a bit tense in parts of the video."
    if face_result["micro_anger_count"] > 0:
      micro_anger = "You still seem a bit angry in parts of the video."

    result = json.dumps({
			"tense": tense,
			"anger": anger,
			"micro_tense": micro_tense,
			"micro_anger": micro_anger
		})

    return HttpResponse(result)
