import os

from InitialFaceRecognition import *
from ImageUnpack import *
from interpret import *
from detect import *
from PYemail import getCredentials


if __name__ == "__main__":

	alreadyWritten = []

	while True:
		inp = input()
		if inp == 'stop':
			break
		#Pull images
		saveFolder = 'attachments'
		path = "../berginRecieverCredentials.json"
		username, password, success = getCredentials(path)
		if success:
			unpack(username, password, saveFolder)
			print('Logged into email')
		else:
			print('Could not find credentials')

		newImages = os.listdir('attachments')

		if len(newImages) == 0:
			print('No new images')
			continue

		client = vision.ImageAnnotatorClient()

		faceImages = []
		
		for file in newImages:
			print('Found new images')
			#Check if they have faces
			if containsFace('attachments/' + file): 
				newImage = Image('attachments/' + file)
				#Run Interpret on those faces 
				newFaces = detect.getFaces('attachments/' + file, client)
				newImage.setFaces(newFaces)
				faceImages.append(newImage)
		for image in faceImages:
			if image not in alreadyWritten:
				file = open('faceData.txt', 'a')
				imageText =('new ' + image.path + ' ' + image.date + ' ' + image.time.hour + ' ' + image.time.minute + '\n')
				file.write(imageText)
				for face in image.faces:
					i = 0
					panAngle = face.pan_angle
					tiltAngle = face.tilt_angle
					detectionConfidence = face.detection_confidence
					landmarkingConfidence = face.landmarking_confidence
					joyLikelihood = face.joy_likelihood
					sorrowLikelihood = face.sorrow_likelihood
					angerLikelihood = face.anger_likelihood
					surpriseLikelihood = face.surprise_likelihood
					underExposedLikelihood = face.under_exposed_likelihood
					blurredLikelihood = face.blurred_likelihood
					headwearLikelihood = face.headwear_likelihood
					faceText = ('image' + str(i) + ' ' + panAngle + ' ' + tiltAngle + ' ' + detectionConfidence + ' ' + landmarkingConfidence + 
					' ' + joyLikelihood + ' ' + sorrowLikelihood + ' ' + angerLikelihood + ' ' + angerLikelihood + ' ' + surpriseLikelihood + 
					' ' + underExposedLikelihood + ' ' + blurredLikelihood + ' ' + headwearLikelihood + '\n')
					file.write(faceText)
					print('Image logged to file')
			file.close()
