import os
import datetime

months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
		 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

class Image:

	def __init__(self, path):
        self.path = path
        self.faces = []
        pathSplit = split(' ')
        self.date = date(int(pathSplit[4][:4]), months[pathSplit[2]], int(pathSplit[3]))
        self.time.hour = path[:2]
        self.time.minute = path[3:5]

    def setFaces(self, myfaces):
		self.faces = myfaces
	def getFaces(self):
		return faces






