import requests
from rhetoric.apis.speechanalyzer.yt_audio_extractor import get_audio
from rhetoric.apis.speechanalyzer.speech_to_text import extract_text
from rhetoric.apis.speechanalyzer.config import GRAMMARBOT_API_KEY

def process_speech(video_url):
    AUDIO_FILE = get_audio(video_url)
    TEXT = extract_text(AUDIO_FILE)

    try:
        r = requests.post('http://bark.phon.ioc.ee/punctuator', data = {'text':TEXT})
        # print(r.text)
    except:
        context = { 'error_msg': 'There\'s an error with the punctuator, try analyzing with google API instead' }
        return context
        # template = loader.get_template('speech/error.html')
        # return HttpResponse(template.render(context, request))

    PUNCTUATED_TEXT = r.text

    try:
        r = requests.get('http://api.grammarbot.io/v2/check?api_key=' + GRAMMARBOT_API_KEY + '&text=' + PUNCTUATED_TEXT + '&language=en')
        RESULT = r.json()
        # print(RESULT)
    except:
        context = { 'error_msg': 'There\'s an error with grammarbot, try analyzing with google API instead' }
        return context
        # print('There\'s an error with grammarbot')
        # template = loader.get_template('speech/error.html')
        # return HttpResponse(template.render(context, request))

def main(video_url):
    result = process_speech(video_url)
    return result
    

