import face_recognition
from PIL import Image, ImageDraw

def containsFace(path):
	image = face_recognition.load_image_file(path)
	face_locations = face_recognition.face_locations(image)

	if(len(face_locations) != 0):
		return(True)
	return(False)

def drawFaces(path):
	image = face_recognition.load_image_file(path)

	face_locations = face_recognition.face_locations(image)
	face_encodings = face_recognition.face_encodings(image, face_locations)

	pil_image = Image.fromarray(image)
	draw = ImageDraw.Draw(pil_image)

	for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
	    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
	del draw
	slashInd = path.find('/')
	imageName = path[slashInd:len(path)-1]

	# Display the resulting image
	pil_image.show()
	pil_image.save('BORDERS' + imageName)

#print(containsFace('images/chair.jpg'))
	