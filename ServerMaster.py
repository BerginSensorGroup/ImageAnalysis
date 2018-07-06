import os

from InitialFaceRecognition import *
from ImageUnpack import *
from interpret import *
from detect import *
from Image import *
from PYemail import getCredentials
import time
import datetime
import os

def window_string(start_window, end_window):
	'''
	Returns a path-friendly string from a time range
	
	Parameters:
	start_window: a datetime object
	end_window: a datetime object occuring after start_window
	'''
	start_str = str(start_window.year) + ' ' + str(start_window.month) + ' ' \
			+ str(start_window.day) + ' ' + str(start_window.hour) + ' ' + \
			str(start_window.minute)
	end_str = str(end_window.year) + ' ' + str(end_window.month) + ' ' \
			+ str(end_window.day) + ' ' + str(end_window.hour) + ' ' + \
			str(end_window.minute)
	return start_str + '_to_' + end_str + '.txt'

def save_metadata_text(faceImages, faceDataFolder = 'faceData', window = 60):
	'''
	Saves image metadata to txt files based on when the images were captured
	
	Parameters:
	
	faceImages: a list of face metadata in the format returned by Google Cloud Vision API
	faceDataFolder: the folder to which the metadata files should be saved
	window: the window of time (in minutes, max 60) with which images should be associated
	'''
	
	#sort faceImages by time captured
	faceImages.sort()
	
	if len(faceImages) > 0:
		start_window =  faceImages[0].datetime
		#remove minutes beyond modulo so no file names cross over
		#between runs (eg 15:35 -> 15:30 for a window of 15)
		start_window = start_window - datetime.timedelta(minutes = start_window.minute%window)
		end_window = start_window + datetime.timedelta(minutes = window)
	
	#go through each image and save its meta data to a text file
	for image in faceImages:
		#when the current image capture time is beyond the alotted capture time for the
		#current textfile, update the alotted capture time to save to a new file
		#to keep the allotted capture times consistent, make them modulo the defined window
		while image.datetime >= end_window:
			start_window = end_window
			end_window = start_window + datetime.timedelta(minutes = window)
		file = open(faceDataFolder+'/'+window_string(start_window, end_window), 'a+')
		imageText = ('image timestamp: ' + image.getDateTimeStr() + '\n')
		file.write(imageText)
		#save each face's metadata for later analysis
		for face in image.getFaces():
			i = 0
			panAngle = str(face.pan_angle)
			tiltAngle = str(face.tilt_angle)
			detectionConfidence = str(face.detection_confidence)
			landmarkingConfidence = str(face.landmarking_confidence)
			joyLikelihood = str(face.joy_likelihood)
			sorrowLikelihood = str(face.sorrow_likelihood)
			angerLikelihood = str(face.anger_likelihood)
			surpriseLikelihood = str(face.surprise_likelihood)
			underExposedLikelihood = str(face.under_exposed_likelihood)
			blurredLikelihood = str(face.blurred_likelihood)
			headwearLikelihood = str(face.headwear_likelihood)
			faceText = ('face' + str(i) + ' ' + panAngle + ' ' + tiltAngle + ' ' + detectionConfidence + ' ' + landmarkingConfidence + 
			' ' + joyLikelihood + ' ' + sorrowLikelihood + ' ' + angerLikelihood + ' ' + angerLikelihood + ' ' + surpriseLikelihood + 
			' ' + underExposedLikelihood + ' ' + blurredLikelihood + ' ' + headwearLikelihood + '\n')
			file.write(faceText)
			print('Face logged to file')
			i += 1
		print('Image logged to file')
		file.close()

if __name__ == "__main__":
	#TODO: after successful tests, delete when image meta data from saveFolder saved
	
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '../Credentials/service-account-file.json'
	
	while True:
		inp = input('enter stop to stop: ')
		if inp == 'stop':
			break
		
		saveFolder = 'attachments'
		credential_path = "../berginRecieverCredentials.json"
		accepted_senders = ['berginsender@gmail.com', 'berginsender2@gmail.com', 'berginsender3@gmail.com','berginsender4@gmail.com']
		
		newImages = downloadImages(saveFolder, credential_path, accepted_senders)

		if len(newImages) == 0:
			print('No new images')
			#if there aren't any new images wait a few seconds before checking again
			time.sleep(15)
			continue

		client = vision.ImageAnnotatorClient()

		faceImages = []
		
		#use SENT and SEND_LIMIT to cap how many pictures we send to Google Cloud for analysis
		QUERY_LIMIT = 10
		QUERIES = 0
		for image_path in newImages:
			print('Running local facial detection on new image')
			#Locally check if they have faces
			if containsFace(saveFolder + '/' + image_path) and QUERIES < QUERY_LIMIT:
				#note Image is our Image class, NOT the Image module from PIL
				newImage = Image(saveFolder + '/' + image_path)
				#Query Google for sentiments of those faces
				newFaces = getFaces(saveFolder + '/' + image_path, client)
				QUERIES += 1
				#Add the image to faceImages only if Google IDs faces
				if len(newFaces) > 0:
					newImage.setFaces(newFaces)
					faceImages.append(newImage)
		
		save_metadata_text(faceImages, window = 60)	