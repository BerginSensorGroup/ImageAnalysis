from picamera import PiCamera

from time import sleep

def takePicture(camera, save_folder, number_file):
	'''
	Parameters
	camera: the camera instance with which to take pictures
	number_file: a file that holds the current picture number so no two pictures
		will ever have the same name. A file is used instead of a variable so
		the number is maintained in the case of power loss
	'''
	pic_num = 0
	try:
		file = open(number_file, 'r')
		pic_num = int(file.read())
		file.close()
	except IOError:
		pass
		
	camera.capture(save_folder + ('{}.jpg',format(pic_num)))
	pic_num += 1
	
	file = open(number_file, 'w+')
	file.write(str(pic_num))