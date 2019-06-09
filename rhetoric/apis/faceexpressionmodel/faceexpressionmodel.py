from JudgeYou.settings import RHETORIC_APP_ROOT, HEROKU_RHETORIC_APP_ROOT
from imutils.video import VideoStream
from keras.preprocessing import image
from django.http import HttpResponse
import tensorflow as tf
import numpy as np
import youtube_dl
import imutils
import time
import cv2
import os
if os.path.isdir(RHETORIC_APP_ROOT):
	MODEL_FOLDER = os.path.join(RHETORIC_APP_ROOT , 'faceexpressionmodel', 'model')
elif os.path.isdir(HEROKU_RHETORIC_APP_ROOT):
	MODEL_FOLDER = os.path.join(HEROKU_RHETORIC_APP_ROOT , 'faceexpressionmodel', 'model')

def process_video(video_url):
	try:
		# Define paths
		prototxt_path = os.path.join(MODEL_FOLDER , 'deploy.prototxt')
		caffemodel_path = os.path.join(MODEL_FOLDER , 'weights.caffemodel')
		model = tf.keras.models.load_model(os.path.join(MODEL_FOLDER , 'cnn_face_expression.model'))
		emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')

		ydl_opts = {}

		# create youtube-dl object
		ydl = youtube_dl.YoutubeDL(ydl_opts)

		# set video url, extract video information
		info_dict = ydl.extract_info(video_url, download=False)

		# get video formats available
		formats = info_dict.get('formats',None)
		title = info_dict.get('title', None)

		flag_for_testing = 0

		def secondMaxEmotion(predictions, max_index):
			emotions_index = 0
			secondary_emotion_index = 0
			max_emotion_num = -1
			for x in predictions:
				if (max_emotion_num < x) and (emotions_index != max_index):
					secondary_emotion_index = emotions_index
					max_emotion_num = x
				emotions_index += 1
				
			for x in predictions:
				if (max_emotion_num < x) and (emotions_index != max_index):
					max_emotion_num = x
				emotions_index += 1

			return secondary_emotion_index

		for f in formats:
			if flag_for_testing == 1:
				break

			# set resolution as 144p
			if f.get('format_note',None) == '144p':
					
				#get the video url
				url = f.get('url',None)

				# load our serialized model from disk
				print("[INFO] loading model...")
				net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)

				# initialize the video stream and allow the cammera sensor to warmup
				print("[INFO] starting video stream...")
				vs = cv2.VideoCapture(url)

				fps = vs.get(cv2.CAP_PROP_FPS)

				frame_count = 0
				emotion_timestamp = []
				emotion_start = -1
				curr_emotion = ""
				# loop over the frames from the video stream
				while True:
					frame_count = frame_count + 1
					# grab the frame from the threaded video stream and resize it
					# to have a maximum width of 400 pixels
					ret, frame = vs.read()
					
					# check if frame is empty
					if not ret:
						break
					
					# grab the frame dimensions and convert it to a blob
					(h, w) = frame.shape[:2]
					blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
						(300, 300), (104.0, 177.0, 123.0))
				
					# pass the blob through the network and obtain the detections and
					# predictions
					net.setInput(blob)
					detections = net.forward()

					sum_confidence = 0
					# loop over the detections
					for i in range(0, detections.shape[2]):
						# extract the confidence (i.e., probability) associated with the
						# prediction
						confidence = detections[0, 0, i, 2]

						# filter out weak detections by ensuring the `confidence` is
						# greater than the minimum confidence
						if confidence < 0.5:
							continue

						sum_confidence = sum_confidence + confidence
						# compute the (x, y)-coordinates of the bounding box for the
						# object
						box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
						(startX, startY, endX, endY) = box.astype("int")
				
						y = startY - 10 if startY - 10 > 10 else startY + 10


					if sum_confidence < 0.6:
						emotion_end = float(frame_count)/fps
						# if face detection confidence is below 50% and the face detected index is not 0 then append face detected duration to tense_timestamp
						if emotion_start != -1:
							emotion_timestamp.append( {'start_time': emotion_start , 'end_time': emotion_end  , 'emotion': curr_emotion} )
							emotion_start = -1

					else:
						detected_face = frame[int(startY):int(startY+endY), int(startX):int(startX+endX)] #crop detected face
						detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY) #transform to gray scale
						detected_face = cv2.resize(detected_face, (48, 48)) #resize to 48x48

						img_pixels = image.img_to_array(detected_face)
						img_pixels = np.expand_dims(img_pixels, axis = 0)
						
						img_pixels /= 255
						
						predictions = model.predict(img_pixels)
						
						#find max indexed array
						max_index = np.argmax(predictions[0])
						secondary_max_index = secondMaxEmotion(predictions[0], max_index)
						
						emotion = emotions[max_index]
						secondary_emotion = emotions[secondary_max_index]

						if (emotion == 'fear' and secondary_emotion == 'sad') or (emotion == 'sad' and secondary_emotion == 'fear'):
							emotion = 'tense'
						elif(emotion == 'angry' and secondary_emotion == 'sad') or (emotion == 'sad' and secondary_emotion == 'angry'):
							emotion = 'serious'

						# if face detection confidence is above 50% and the face detected index is 0 then set new face detected index
						if emotion_start == -1:
							emotion_start = float(frame_count)/fps
							curr_emotion = emotion
						# if emotion change then add anger_timestamp
						elif curr_emotion != emotion and emotion_start != -1:
							emotion_end = float(frame_count)/fps
							emotion_timestamp.append( {'start_time': emotion_start ,'end_time': emotion_end ,'emotion': emotion} )
							emotion_start = -1
							curr_emotion = emotion
						# if video end then add anger_timestamp
						if frame_count == fps and emotion_start != -1:
							emotion_end = float(frame_count)/fps
							emotion_timestamp.append( {'start_time': emotion_start ,'end_time': emotion_end ,'emotion': curr_emotion} )
							break

					flag_for_testing = 1

				if flag_for_testing == 1:
					break

		vs.release()

		tense_count = 0
		tense_timestamp = {
			"start_time": 0,
			"end_time": 0
		}
		micro_tense_count = 0
		micro_tense_timestamp = {
			"1":{
				"start_time": 0,
				"end_time": 0
			},
			"2":{
				"start_time": 0,
				"end_time": 0
			},
			"3":{
				"start_time": 0,
				"end_time": 0
			}
		}
		anger_count = 0
		anger_timestamp = {
			"start_time": 0,
			"end_time": 0
		}
		micro_anger_count = 0
		micro_anger_timestamp = {
			"1":{
				"start_time": 0,
				"end_time": 0
			},
			"2":{
				"start_time": 0,
				"end_time": 0
			},
			"3":{
				"start_time": 0,
				"end_time": 0
			}
		}
		for x in emotion_timestamp:
			if x["end_time"] - x["start_time"] >= 0.5 and x["emotion"] == 'tense':
				tense_count += 1
				if tense_timestamp["end_time"] - tense_timestamp["start_time"] < x["end_time"] - x["start_time"]:
					tense_timestamp["start_time"] = x["start_time"]
					tense_timestamp["end_time"] = x["end_time"]

			if x["end_time"] - x["start_time"] >= 0.1 and x["end_time"] - x["start_time"] < 0.5 and x["emotion"] == 'tense':
				micro_tense_count += 1
				if micro_tense_timestamp["1"]["end_time"] - micro_tense_timestamp["1"]["start_time"] < x["end_time"] - x["start_time"]:
					micro_tense_timestamp["3"]["start_time"] = micro_tense_timestamp["2"]["start_time"]
					micro_tense_timestamp["3"]["end_time"] = micro_tense_timestamp["2"]["end_time"]
					micro_tense_timestamp["2"]["start_time"] = micro_tense_timestamp["1"]["start_time"]
					micro_tense_timestamp["2"]["end_time"] = micro_tense_timestamp["1"]["end_time"]
					micro_tense_timestamp["1"]["start_time"] = x["start_time"]
					micro_tense_timestamp["1"]["end_time"] = x["end_time"]
			
			if x["end_time"] - x["start_time"] >= 0.5 and x["emotion"] == 'angry':
				anger_count += 1
				if anger_timestamp["end_time"] - anger_timestamp["start_time"] < x["end_time"] - x["start_time"]:
					anger_timestamp["start_time"] = x["start_time"]
					anger_timestamp["end_time"] = x["end_time"]
			
			if x["end_time"] - x["start_time"] >= 0.1 and x["end_time"] - x["start_time"] < 0.5 and x["emotion"] == 'angry':
				micro_anger_count += 1
				if micro_anger_timestamp["1"]["end_time"] - micro_anger_timestamp["1"]["start_time"] < x["end_time"] - x["start_time"]:
					micro_anger_timestamp["3"]["start_time"] = micro_anger_timestamp["2"]["start_time"]
					micro_anger_timestamp["3"]["end_time"] = micro_anger_timestamp["2"]["end_time"]
					micro_anger_timestamp["2"]["start_time"] = micro_anger_timestamp["1"]["start_time"]
					micro_anger_timestamp["2"]["end_time"] = micro_anger_timestamp["1"]["end_time"]
					micro_anger_timestamp["1"]["start_time"] = x["start_time"]
					micro_anger_timestamp["1"]["end_time"] = x["end_time"]

		
		result = {
			"title": title,
			"tense_count": tense_count,
			"anger_count": anger_count,
			"micro_tense_count": micro_tense_count,
			"micro_anger_count": micro_anger_count,
			"tense_timestamp": tense_timestamp,
			"anger_timestamp": anger_timestamp,
			"micro_tense_timestamp": micro_tense_timestamp,
			"micro_anger_timestamp": micro_anger_timestamp,
			"error": False
		}

		return result
				
	except Exception as e:
		err_msg = { 
			"err_msg":str(e),
			"error": True
		}

		return err_msg


def main(video_url):
    result = process_video(video_url)
    return result