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
	    # See if the face is a match for the known face(s)
	    #matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
	    #name = "Unknown"

	    # If a match was found in known_face_encodings, just use the first one.
	    #if True in matches:
	        #first_match_index = matches.index(True)
	        #name = known_face_names[first_match_index]

	    # Draw a box around the face using the Pillow module
	    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

	    # Draw a label with a name below the face
	    #text_width, text_height = draw.textsize(name)
	    #draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
	    #draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
	del draw
	slashInd = path.find('/')
	imageName = path[slashInd:len(path)-1]

	# Display the resulting image
	pil_image.show()
	pil_image.save('BORDERS' + imageName)

#print(containsFace('images/chair.jpg'))
for i in range(150, 155):
	x = containsFace('frames/frame' + str(i) + '.jpg')
	if x:
		print('\n')
		print(str(i))
		print(x)
		drawFaces('frames/frame' + str(i) + '.jpg')
	