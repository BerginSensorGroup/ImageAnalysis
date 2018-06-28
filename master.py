import PYemail
import camera_controller
from picamera import PiCamera
import threading
import datetime
from time import sleep
import os
import smtplib
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

def camera_run_json(camera, current_json_folder, unsent_json_folder, unsent_picture_folder, picture_number_file, name, call_freq = 10.0):
    '''
    Takes a picture every call_freq seconds
    
    Parameters
    camera: the camera instance with which to take pictures
    save_folder: the folder to which to save the picture
    number_file: a file that holds the current picture number so no two pictures
        will ever have the same name. A file is used instead of a variable so
        the number is maintained in the case of power loss
    '''
    try:
		MIN_SPACE = 100000000 #don't take a picture unless we have at least 100 MB of free space
		if have_more_space_than(MIN_SPACE):
			camera_controller.takePicture_use_json(camera, current_json_folder, unsent_json_folder, unsent_picture_folder, picture_number_file, name)
	
		t = threading.Timer(call_freq, camera_run_json, (camera, current_json_folder, unsent_json_folder, unsent_picture_folder, picture_number_file, name))
		t.daemon = True #finish when main finishes
		t.start()
    except:
        #if there are any uncaught exceptions we need to kill the program for debugging
	    recordFailure()
	    #send a keyboard interrupt to main thread
	    os.kill(os.getpid(), signal.SIGINT)

def sending_run(username, password, receiver, send_folder, stamp_folder):
    '''
    Attempts to send all the files in send_folder via email
    If successful function repeats after 60 seconds
    If unsuccessful function repeates after 30 seconds
    
    Parameters:
    username: the email account sending the message
    password: the password of the username account
    receiver: the email account receiveing the message
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

def sending_run_json(credentials, receiver, unsent_json_folder):
    '''
    Attempts to send all the pictures from the paths in the jsons contained in
        unsent_json_folder
    If successful, function repeats after 60 seconds
    If unsuccessful, function repeates after 30 seconds
    
    Parameters:
    credentials: a credential_set object containing credentials with which to send emails
    receiver: the email account receiveing the message
    unsent_json_folder: the directoty from which to obtain the files to send
    '''
    try:
		json_paths = os.listdir(unsent_json_folder)
		json_paths = [unsent_json_folder + file_name for file_name in json_paths]
   
		seconds_until_next_call = 0
		if PYemail.have_internet():
			host_address, port_number, username, password = credentials.getCurrentCredentials()
			server = PYemail.setupSMTP(host_address, port_number, username, password)
			if server != None:
				sent_all = False
				try:
					sent_all = PYemail.sendAllJson(username, receiver, json_paths, server, delete_sent = True)
				except smtplib.SMTPDataError:
					#SMTPDataError exception likely happened because we exceeded the quota of our email provider
					credentials.updateExpiration()
				except smtplib.SMTPSenderRefused:
					#SMTPSenderRefused exception likely happened because we sent too many messages on one SMTP instance
					#this will resolve itself when we open the next SMTP instance
					pass
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
		t = threading.Timer(seconds_until_next_call, sending_run_json, (credentials, receiver, unsent_json_folder))
		t.daemon = True #finish when main finishes
		t.start()
	except:
	    #if there are any uncaught exceptions we need to kill the program for debugging
	    recordFailure()
	    #send a keyboard interrupt to main thread
	    os.kill(os.getpid(), signal.SIGINT)

def recordFailure():
    #Record the reason why the program terminated
    #exception_type, exception_value, traceback = sys.exc_info()
    termination_log = open(termination_log_path, 'a+')
    termination_log.write('Date: '+ datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n')
    termination_log.write("\tConnected to internet: " + str(PYemail.have_internet()) + '\n')
    termination_log.write(traceback.format_exc())
    termination_log.write("\n\n\n\n\n")
    termination_log.close()   

def main1():
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
        recordFailure()

def main2():
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
        
        current_json_folder = '/home/pi/Documents/facial_detection/current_json_folder/'
        unsent_json_folder = '/home/pi/Documents/facial_detection/unsent_json_folder/'
        unsent_picture_folder = '/home/pi/Documents/facial_detection/unsent_pictures/'
        picture_number_file = '/home/pi/Documents/facial_detection/current_picture_number.txt'
        
        send_credentials_folder = "../Credentials/sending_credentials/"
        
        credential_paths = os.listdir(send_credentials_folder)
        credential_paths = [send_credentials_folder + json_name for json_name in credential_paths]
        
        receiver = 'BerginReciever@gmail.com'
    
        camera = PiCamera()
        
        '''
        There are some camera settings we could play around with:
        camera = PiCamera(resolution=(1280, 720),framerate=Fraction(1, 6),sensor_mode=3)
		camera.shutter_speed = 6000000
		camera.iso = 800
        
        https://picamera.readthedocs.io/en/release-1.13/recipes1.html
        For low light suggests low framerate (1/6 fps), slow shutter speed (6s), and high ISO (800)
        '''
        
        
        valid_credentials = PYemail.credential_set()
        for credential_path in credential_paths:
            host_addr, port_num, username, password, credentials_OK = PYemail.getCredentials(credential_path)
            if credentials_OK:
                 valid_credentials.addCredential(host_addr, port_num, username, password)
        
        #wait 15 seconds on startup for wifi to connect
        if not PYemail.have_internet():
            sleep(15)
        
        camera_run_json(camera, current_json_folder, unsent_json_folder, unsent_picture_folder, picture_number_file, name)
        
        if credentials_OK:
            sending_run_json(valid_credentials, receiver, unsent_json_folder)
        
        while True:
            pass
    except:
       recordFailure()
            
if __name__ == '__main__':
    main2()
