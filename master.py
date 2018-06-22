import PYemail
import camera_controller
from picamera import PiCamera
import threading
import datetime
from time import sleep
import os
import sys
import traceback
from disk_space import have_more_space_than

def camera_run(camera, save_folder, stamp_folder, picture_number_file, name, call_freq = 10.0):
    '''
    Takes a picture every call_freq seconds
    
    Parameters
    camera: the camera instance with which to take pictures
    save_folder: the folder to which to save the picture
    number_file: a file that holds the current picture number so no two pictures
        will ever have the same name. A file is used instead of a variable so
        the number is maintained in the case of power loss
    '''
    MIN_SPACE = 100000000 #don't take a picture unless we have at least 100 MB of free space
    if have_more_space_than(MIN_SPACE):
        camera_controller.takePicture(camera, save_folder, stamp_folder, picture_number_file, name)
    
    t = threading.Timer(call_freq, camera_run, (camera, save_folder, stamp_folder, picture_number_file, name))
    t.daemon = True #finish when main finishes
    t.start()

def sending_run(username, password, receiver, send_folder, stamp_folder):
    '''
    Attempts to send all the files in send_folder via email
    If successful function repeats after 60 seconds
    If unsuccessful function repeates after 30 seconds
    
    Parameters:
    username: the email account sending the message
    password: the password of the username account
    reciever: the email account receiveing the message
    send_folder: the directoty from which to obtain the files to send
    '''

    to_send = os.listdir(send_folder)
    to_send = [send_folder + file_name for file_name in to_send]
    stamp_paths = os.listdir(stamp_folder)
    stamp_paths = [stamp_folder + file_name for file_name in stamp_paths]
    
    seconds_until_next_call = 0
    if PYemail.have_internet():
        server = PYemail.setupSMTP(host_address, port_number, username, password)
        if server != None:
            sent_all = PYemail.sendAll(username, receiver, to_send, stamp_paths, server)
            if sent_all:
                seconds_until_next_call = 60
                server.quit()
                #sent all files
            else:
                seconds_until_next_call = 30
                #sent some but not all
        else:
            seconds_until_next_call = 30
            #Didn't send any: had internet but could not setup SMTP
    else:
        seconds_until_next_call = 30
        #Didn't send any: did not have internet
    t = threading.Timer(seconds_until_next_call, sending_run, (username, password, receiver, send_folder, stamp_folder))
    t.daemon = True #finish when main finishes
    t.start()
        
if __name__ == '__main__':
    try:
        ##CONSTANTS
        #path of termination log, must be the same as in on_termination.py
        termination_log_path = 'TERMINATION_LOG.txt'
        
        #unique name of this Pi
        name_path = 'Name.txt'
        name = 'NAME NOT AVAILABLE'
        try:
            name_file = open(name_path, 'r')
            name = name_file.read()
            name_file.close()
        except IOError:
            #if the name file does not exist, just continue without a name
            pass
        
        save_folder = '/home/pi/Documents/facial_detection/unsent_pictures/'
        stamp_folder = '/home/pi/Documents/facial_detection/unsent_stamps/'
        picture_number_file = '/home/pi/Documents/facial_detection/current_picture_number.txt'
        
        credentials_path = "../Credentials/berginSenderCredentials.json"
        receiver = 'BerginReciever@gmail.com'
        #GMAIL TO GENERAL EXCHANGE (SMTP TLS)
        host_address = "smtp.gmail.com"
        port_number = 587
        
        ##END CONSTANTS
        
        camera = PiCamera()
        
        username, password, credentials_OK = PYemail.getCredentials(credentials_path)
        
        #wait 15 seconds on startup for wifi to connect
        if not PYemail.have_internet():
            sleep(15)
        
        camera_run(camera, save_folder, stamp_folder, picture_number_file, name)
        
        if credentials_OK:
            sending_run(username, password, receiver, save_folder, stamp_folder)
        
        while True:
            pass
    except:
		#Record the reason why the program terminated
        #exception_type, exception_value, traceback = sys.exc_info()
        termination_log = open(termination_log_path, 'a+')
        termination_log.write('Date: '+ datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n')
        termination_log.write("\tConnected to internet: " + str(PYemail.have_internet()) + '\n')
        termination_log.write(traceback.format_exc())
        termination_log.write("\n\n\n\n\n")
        termination_log.close()
