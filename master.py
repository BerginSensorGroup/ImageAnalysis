import PYemail
import camera_controller
from picamera import PiCamera
import threading
import datetime

def camera_run(camera, save_folder, stamp_folder, picture_number_file):
    '''
    Takes a picture every 60 seconds
    
    Parameters
    camera: the camera instance with which to take pictures
    save_folder: the folder to which to save the picture
    number_file: a file that holds the current picture number so no two pictures
        will ever have the same name. A file is used instead of a variable so
        the number is maintained in the case of power loss
    '''
    camera_controller.takePicture(camera, save_folder, picture_number_file)
    now = datetime.datetime.now()
    time_stamp_path = stamp_folder + ('{}.txt'.format(pic_num))
    time_stamp_file = open(time_stamp_path, 'w+')
    #Either store the current time for the picture or declare that we do not know the time
    if now.year < 2018:
        time_stamp_file.write('NO TIME (time unknown when picture was taken)')
    else:
        time_stamp_file.write(now.strftime("%I:%M%p on %B %d, %Y"))
    time_stamp_file.close()
    t = threading.Timer(60.0, camera_run, (camera, save_folder, stamp_folder, picture_number_file))
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
    stamp_paths = os.listdir(send_folder)
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
    ##CONSTANTS
    
    save_folder = '/home/pi/Documents/facial_detection/unsent_pictures/'
    stamp_folder = '/home/pi/Documents/facial_detection/unsent_stamps/'
    picture_number_file = '/home/pi/Documents/facial_detection/current_picture_number.txt'
    
    credentials_path = "berginSenderCredentials.json"
    receiver = 'BerginReciever@gmail.com'
    #GMAIL TO GENERAL EXCHANGE (SMTP TLS)
    host_address = "smtp.gmail.com"
    port_number = 587
    
    ##END CONSTANTS
    
    camera = PiCamera()
    
    username, password, credentials_OK = PYemail.getCredentials(credentials_path)
    
    camera_run(camera, save_folder, stamp_folder, picture_number_file)
    
    if credentials_OK:
        sending_run(username, password, receiver, save_folder, stamp_folder)
    
    while True:
        pass
