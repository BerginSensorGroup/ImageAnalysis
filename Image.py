import os
import datetime

months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
		 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

class Image:

	def __init__(self, path, name):
        self.name = name
        self.path = path

        pathSplit = split(' ')
        self.date = date(int(pathSplit[4][:4]), months[pathSplit[2]], int(pathSplit[3])
        



