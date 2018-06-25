from picamera import PiCamera
import datetime
import json
import string
import random
import os
import shutil

def takePicture(camera, save_folder, stamp_folder, number_file, name):
    '''
    Parameters
    camera: the camera instance with which to take pictures
    number_file: a file that holds the current picture number so no two pictures
        will ever have the same name. A file is used instead of a variable so
        the number is maintained in the case of power loss
    
    Returns the picture number that was saved
    '''
    pic_num = 0
    try:
        file = open(number_file, 'r')
        pic_num = int(file.read())
        file.close()
    except IOError:
        #if we get IOError here, that means the file did not yet exist
        #in this case just start pic_num at zero
        pass
    
    now = datetime.datetime.now()    
        
    camera.capture(save_folder + ('{}_{}.jpg'.format(name,pic_num)))
    
    time_stamp_path = stamp_folder + ('{}.txt'.format(pic_num))
    time_stamp_file = open(time_stamp_path, 'w+')
    #Either store the current time for the picture or declare that we do not know the current time
    #Note that if we don't have the time, the default time is the beginning of Unix time (1970)
    if now.year < 2018:
        time_stamp_file.write('NO TIME (time unknown when picture was taken)')
    else:
        time_stamp_file.write(now.strftime("%I_%M%p on %B %d %Y"))
    time_stamp_file.close()
    
    #finish the function by updating the picture number
    pic_num += 1
    
    file = open(number_file, 'w+')
    file.write(str(pic_num))
    file.close()

def takePicture_use_json(camera, current_json_folder, unsent_json_folder, unsent_picture_folder, number_file, name):
    '''
    Parameters
    camera: the camera instance with which to take pictures
    current_json_folder: the folder with the json containing the filepaths of pictures
    	taken in the current minute
    unsent_json_folder: the folder with jsons containing the file
    number_file: a file that holds the current picture number so no two pictures
        will ever have the same name. A file is used instead of a variable so
        the number is maintained in the case of power loss
    name: the unique name of the Raspberry Pi
    
    Returns the picture number that was saved
    '''
    pic_num = 0
    try:
        file = open(number_file, 'r')
        pic_num = int(file.read())
        file.close()
    except IOError:
        #if we get IOError here, that means the file did not yet exist
        #in this case just start pic_num at zero
        pass
    now = datetime.datetime.now()
    picture_path = unsent_picture_folder + ('{}_{}.jpg'.format(name,pic_num))
    camera.capture(picture_path)
    current_time_string = now.strftime("%I_%M%p on %B %d %Y")
    
    
    #get path from current_json_folder, if it is empty then make a new
    #files should be empty or contain one file
    files_in_current_folder = os.listdir(current_json_folder)
    if len(files_in_current_folder) == 1:
        current_json_path = current_json_folder + files_in_current_folder[0]
        json_file = open(current_json_path, 'r')
        json_str = json_file.read()
        json_file.close()
        picture_data = json.loads(json_str)
        old_time_string = picture_data["taken"]
        #	if they are the same time string append picture_path to the array and save the json
        if old_time_string == current_time_string:
            picture_data["picture_paths"].append(picture_path)
            with open(current_json_path, 'w') as savefile:
            	json.dump(picture_data, savefile)
        #	if they are different move the old json to unsent_json_folder and make a new json file holding the time and picture
        else:
            #transfer the file to the unsent folder
            shutil.move(current_json_path, unsent_json_folder + files_in_current_folder[0])
            current_json_path = unsent_json_folder + current_time_string +'.json'
            #set up a dictionary to save to a new json file
            new_data = {"taken": current_time_string, "picture_paths" : [picture_path]}
            with open(current_json_path, 'w+') as savefile:
                json.dump(new_data, savefile)
    elif len(files_in_current_folder) == 0:
        #make a new json file to put within the current folder
        new_data = {"taken": current_time_string, "picture_paths" : [picture_path]}
        current_json_path = current_json_folder + current_time_string +'.json'
        with open(current_json_path, 'w+') as savefile:
                json.dump(new_data, savefile)
    else:
        #otherwise ERROR: there are more than one files identified as the current minute
        pass
    
    #finish the function by updating the picture number
    pic_num += 1
    
    file = open(number_file, 'w+')
    file.write(str(pic_num))
    file.close()
    
    
    
