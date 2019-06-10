import json
from . import apis
from rhetoric.models import Review
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
import rhetoric.apis.faceexpressionmodel.faceexpressionmodel as facescoremodel

# Create your views here.

def home(request):
  return render(request, 'rhetoric/home.html')

def upload(request):
  return render(request, 'rhetoric/upload.html')

def commentating(request, yt_id):
  review_details = get_object_or_404(Review, yt_id=yt_id)
  return render_to_response('rhetoric/commentating.html', {'review' : review_details})

def review(request):
  try:
    face_result = facescoremodel.main(request.POST.get("url", ""))
    review = Review.objects.get(yt_id=request.POST.get("id", ""))

    if face_result["error"]:
      review.error = face_result["err_msg"]
      review.save()

      return HttpResponse("Failed")
    else:
      if face_result["tense_count"] > 0:
        review.tense_count = face_result["tense_count"]
        review.tense_timestamp = face_result["tense_timestamp"]
      if face_result["anger_count"] > 0:
        review.anger_count = face_result["anger_count"]
        review.anger_timestamp = face_result["anger_timestamp"]
      if face_result["micro_tense_count"] > 0:
        review.micro_tense_count = face_result["micro_tense_count"]
        review.micro_tense_timestamp = face_result["micro_tense_timestamp"]
      if face_result["micro_anger_count"] > 0:
        review.micro_anger_count = face_result["micro_anger_count"]
        review.micro_anger_timestamp = face_result["micro_anger_timestamp"]
    
      review.title = face_result["title"]
      review.finish_processing = True
      review.save()

      return HttpResponse("Success")
  except Exception as e:
    review.error = str(e)
    review.save()

    return HttpResponse("Failed")
  
def pending(request):
  if request.method == 'POST':
    try:
      if request.POST.get("id", ""):
        post=Review()
        post.yt_id= request.POST.get("id", "")
        post.finish_processing = False
        post.save()

        return HttpResponse("Success")
      else:
        return HttpResponse("Failed: Failed to get video ID")
    except Exception as e:
        return HttpResponse("Failed: " + str(e))
  else:
    return HttpResponse("Failed: Request method not allowed")

def getCommentary(request):
    review = Review.objects.get(yt_id=request.GET.get('id'))
    
    tense = ""
    anger = ""
    micro_tense = ""
    micro_anger = ""

    if review.tense_count > 0:
      tense = "You are seen as tense in some parts of the video, I detected about " + str(review.tense_count) + " moments when you seem tense."

    if review.anger_count > 0:
      anger = "Your seen to be angry in some parts of the video, I counted about " + str(review.anger_count) + " times you looked angry."

    if review.micro_tense_count > 0:
      micro_tense = "You still seem a bit tense in parts of the video."

    if review.micro_anger_count > 0:
      micro_anger = "You still seem a bit angry in parts of the video."

    result = json.dumps({
      "yt_id": review.yt_id,
      "tense": tense,
      "anger": anger,
      "micro_tense": micro_tense,
      "micro_anger": micro_anger,
      "tense_timestamp": review.tense_timestamp,
      "anger_timestamp": review.anger_timestamp,
      "micro_tense_timestamp": review.micro_tense_timestamp,
      "micro_anger_timestamp": review.micro_anger_timestamp
    })

    return HttpResponse(result)