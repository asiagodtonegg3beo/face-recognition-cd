# USAGE
# python recognize_video.py --detector face_detection_model \
#	--embedding-model openface_nn4.small2.v1.t7 \
#	--recognizer output/recognizer.pickle \
#	--le output/le.pickle

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
from flask import Response
from flask import Flask
from flask import render_template
import threading
import datetime
import numpy as np
import argparse
import imutils
import pickle
import time
import verify as vf
from cv2 import cv2
#import verify as vf
count = 0
state = 0

# load our serialized face detector from disk
print("[INFO] loading face detector...")
protoPath = 'face_detection_model\\deploy.prototxt'
modelPath = 'face_detection_model\\res10_300x300_ssd_iter_140000.caffemodel'
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# load our serialized face embedding model from disk
print("[INFO] loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch('openface_nn4.small2.v1.t7')

# load the actual face recognition model along with the label encoder
recognizer = pickle.loads(open('output\\recognizer.pickle', "rb").read())
le = pickle.loads(open('output\\le.pickle', "rb").read())

# initialize the video stream, then allow the camera sensor to warm up
print("[INFO] starting video stream...")
time.sleep(2.0)

# start the FPS throughput estimator
fps = FPS().start()
# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)

outputFrame = None
lock = threading.Lock()

global ip 
global portnum
ip = '0.0.0.0'
portnum = 600
# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to
# warmup
#vs = VideoStream(usePiCamera=1).start()
time.sleep(2.0)

@app.route("/")
def index():
	# return the rendered template
	return render_template("camera.html")

def detect_motion(frameCount):
	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, outputFrame, lock,lastname,timeindex
	timeindex=0
	lastname=''
	# initialize the motion detector and the total number of frames
	# read thus far
	#md = SingleMotionDetector(accumWeight=0.1)
	#total = 0

	# loop over frames from the video stream
	while True:
		vs = VideoStream('http://192.168.1.115:8080/?action=stream')
		time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
		frame = vs.read()

	# resize the frame to have a width of 600 pixels (while
	# maintaining the aspect ratio), and then grab the image
	# dimensions
		frame = imutils.resize(frame, width=600)
		(h, w) = frame.shape[:2]
	
		cv2.putText(frame,"currentime:"+time1, (20, 20),cv2.FONT_HERSHEY_PLAIN,
    		1.5, (255, 255, 255), 1, cv2.LINE_AA)
	# construct a blob from the image
		imageBlob = cv2.dnn.blobFromImage(
			cv2.resize(frame, (300, 300)), 1.0, (300, 300),
			(104.0, 177.0, 123.0), swapRB=False, crop=False)

	# apply OpenCV's deep learning-based face detector to localize
	# faces in the input image
		detector.setInput(imageBlob)
		detections = detector.forward()
		for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the prediction
			confidence = detections[0, 0, i, 2]

		# filter out weak detections
			if confidence > args["confidence"]:
			# compute the (x, y)-coordinates of the bounding box for
			# the face
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

			# extract the face ROI
				face = frame[startY:endY, startX:endX]
				(fH, fW) = face.shape[:2]

			# ensure the face width and height are sufficiently large
				if fW < 20 or fH < 20:
					continue

			# construct a blob for the face ROI, then pass the blob
			# through our face embedding model to obtain the 128-d
			# quantification of the face
				faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
					(96, 96), (0, 0, 0), swapRB=True, crop=False)
				embedder.setInput(faceBlob)
				vec = embedder.forward()

			# perform classification to recognize the face
				preds = recognizer.predict_proba(vec)[0]
				j = np.argmax(preds)
				proba = preds[j]
				name = le.classes_[j]
				if name == lastname :
					if proba*100 > 30 :
						count+=1
				else :
					count=0
				if count==15:
					count=0
					print('\a')
					print(name,time1)
					#if state == 0:
					#	vf.late(name)
					#else:
					vf.ontime(name)
				lastname=name
			# draw the bounding box of the face along with the
			# associated probability
				text = "{}: {:.2f}%".format(name, proba * 100)
				y = startY - 10 if startY - 10 > 10 else startY + 10
				cv2.rectangle(frame, (startX, startY), (endX, endY),
					(0, 0, 255), 2)
				cv2.putText(frame, text, (startX, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
		with lock:
			outputFrame = frame.copy()
def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock

	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue

			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

			# ensure the frame was successfully encoded
			if not flag:
				continue

		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':
	# construct the argument parser and parse command line arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())
	# start a thread that will perform motion detection
	t = threading.Thread(target=detect_motion, args=(
		args["frame_count"],))
	t.daemon = True
	t.start()
	# start the flask app
	app.run(host=ip, port=portnum, debug=True,
		threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()