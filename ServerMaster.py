import os

from InitialFaceREcognition import *
from ImageUnpack import *
from interpret import *
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
	
	for x in newImages:
		#Check if they have faces
		if containsFace('attachments/' + x): 
			#Run Interpret on those faces 




	
