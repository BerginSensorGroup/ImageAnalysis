import os

from InitialFaceREcognition import *
from ImageUnpack import *
from interpret import *
from detect import *
from PYemail import getCredentials


if __name__ == "__main__":

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
		if containsFace('attachments/' + x): 
			newImage = Image('attachments/' + x)
			#Run Interpret on those faces 
			newImage.setFaces() = getFaces(file, client)
			faceImages.append(newImage)
#TODO: write information to from faceImages
			
			




	
