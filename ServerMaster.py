import os

from InitialFaceREcognition import *
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
		else:
			print('Could not find credentials')

	newImages = os.listdir('attachments')

	if len(newImages) == 0:
		print('No new images')
		continue

	client = vision.ImageAnnotatorClient()

	faceImages = []
	
	for file in newImages:
		#Check if they have faces
		if containsFace('attachments/' + file): 
			newImage = Image('attachments/' + file)
			#Run Interpret on those faces 
			newImage.setFaces() = detect.getFaces('attachments/' + file, client)
			faceImages.append(newImage)
#TODO: write information to from faceImages
'''
face_data["roll_angle"] = faces[face_num].roll_angle
		face_data["pan_angle"] = faces[face_num].pan_angle
		face_data["tilt_angle"] = faces[face_num].tilt_angle
		face_data["detection_confidence"] = faces[face_num].detection_confidence
		face_data["landmarking_confidence"] = faces[face_num].landmarking_confidence
		face_data["joy_likelihood"] = faces[face_num].joy_likelihood
		face_data["sorrow_likelihood"] = faces[face_num].sorrow_likelihood
		face_data["anger_likelihood"] = faces[face_num].anger_likelihood
		face_data["surprise_likelihood"] = faces[face_num].surprise_likelihood
		face_data["under_exposed_likelihood"] = faces[face_num].under_exposed_likelihood
		face_data["blurred_likelihood"] = faces[face_num].blurred_likelihood
		face_data["headwear_likelihood"] = faces[face_num].headwear_likelihood
		faces_data["{}".format(face_num)] = face_data
'''
	for image in faceImages:
		if image not in alreadyWritten:
			file = open('faceData.txt', 'a')
			imageText ='new ' + image.path + ' ' + image.date + ' ' + image.time.hour + ' ' + image.time.minute + '\n'
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
				faceText = 'image' + str(i) + ' ' + panAngle + ' ' + tiltAngle + ' ' + detectionConfidence + ' ' + landmarkingConfidence + 
				' ' + joyLikelihood + ' ' + sorrowLikelihood + ' ' + angerLikelihood + ' ' angerLikelihood + ' ' + surpriseLikelihood + 
				' ' + underExposedLikelihood + ' ' + blurredLikelihood + ' ' + headwearLikelihood + '\n'
				file.write(faceText)
		file.close()



			
			




	
