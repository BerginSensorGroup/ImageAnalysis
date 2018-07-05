import os
import datetime

months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
         'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

class Image:
    def __init__(self, path):
        '''
        Example path: "attachments/01_09PM on June 29 2018_Vanquisher_32998"
        '''
        self.path = path
        self.faces = []
        #Get the time, month, day, year and picture number by splitting the path 
        pathSplit = path.split(' ')
        year_num = int(pathSplit[4][:4])
        month_num = months[pathSplit[2]]
        day_num =  int(pathSplit[3])
        self.date = date(year_num, month_num, day_num)
        time_string = (pathSplit[0].split('/'))[1]
        hour_num = int(time_string[:2])
        if hour_num == 12 and time_string[5:] == 'AM':
            hour_num = 0
        if hour_num != 12 and time_string[5:] == 'PM':
            hour_num += 12
        minute_num = int(time_string[3:5])
        self.time =  time(hour_num, minute_num)

    def setFaces(self, myfaces):
        self.faces = myfaces
    def getFaces(self):
        return faces