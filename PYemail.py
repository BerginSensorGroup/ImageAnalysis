#some code adapted from:
#https://stackoverflow.com/questions/3362600/how-to-send-email-attachments
#and
#https://medium.freecodecamp.org/send-emails-using-code-4fcea9df63f

import json
import smtplib
import os.path as op
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import datetime
import http.client


#this function from:
#https://stackoverflow.com/questions/3764291/checking-network-connection
def have_internet():
    '''
    Returns True if the computer is connected to internet, else False
    '''
    conn = http.client.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False

def setupSMTP(host_address, port_number, username, password):
    '''
    Sets up the SMTP connection
    
    Parameters
    host_address: the email service provider's host_address for SMTP
    port_number: the email service provider's port number for TLS
    user_name: the email address of the sender
    password: the password to the email account of the sender
    '''
    try:
        s = smtplib.SMTP(host= host_address, port= port_number, timeout = 30)
        s.starttls()
        s.login(username, password)
        return s
    except smtplib.SMTPConnectError:
        f = open("ERROR_LOG.txt","a+")
        f.write('Error: Could not setup SMTP connection, will retry in a minute')
        return None

def getCredentials(path):
    '''
    Extracts and returns the username and password from a json in a tuple
    final value in tuple is True if success and False if failure
    
    Parameters
    path: the path of the json to be read
    '''
    try:
        json_file = open(path)
        json_str = json_file.read()
        json_data = json.loads(json_str)
        return json_data["username"], json_data["password"], True
    except IOError:
        f = open("ERROR_LOG.txt","a+")
        f.write('Error: JSON path was invalid. Will not send pictures\n')
        f.close()
        return "","", False

def formatMessage(sender, receiver, files, subject = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")):
    '''
    formats an email message to send by SMTP server
    
    Parameters
    sender: the email account sending the message
    receiver: the email account receiveing the message
    subject: the subject of the email
    files: a list of (str) paths to files that need to be attached
    '''
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg['Date'] = formatdate(localtime=True)
    msg["Subject"] = subject
    
    for path in files:
        with open(path, 'rb') as file:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition','attachment; filename="{}"'.format(op.basename(path)))
            msg.attach(part)
    
    return msg

def get_stamp_and_stamp_path(stamp_paths, file_path){
    '''
    Given the file path, finds the corressponding time stamp in the provided stamp_paths list
    Assumes that the file path ends in /<NUMBER>.ext where <NUMBER> is the desired stamp file number
    '''
    
    for stamp_path in stamp_paths:
        ext_loc = stamp_path.find('.')
        last_slash = stamp_path.rfind('/')
        stamp_number = int(stamp_path[last_slash+1:ext_loc])
        
        ext_loc = file_path.find('.')
        last_slash = file_path.rfind('/')
        file_number = int(file_path[last_slash+1:ext_loc])
        
        if stamp_number == file_number:
            with f as open(stamp_file, 'r'):
                return (f.read(), stamp_file)
    
    return ('NO TIME (could not find stamp file)', 'THIS_IS_NOT_A_FILE_PATH')

def sendAll(sender, receiver, file_paths, stamp_paths, server, delete_sent = True):
    '''
    Attempts to send all files located at the paths in file_paths via email
    
    sender: the email account sending the message
    receiver: the email account receiveing the message
    file_paths: a list of (str) paths to files that need to be sent
    delete_sent: should we delete the file after it is successfully emailed
    '''
    for file_path in file_paths:
        subject, stamp_path = get_stamp_and_stamp_path(stamp_paths, file_path)
        msg = formatMessage(sender, receiver, [file_path], subject)
        try:
            server.send_message(msg)
            if delete_sent:
                os.remove(file_path)
                #also try to delete stamp file
                if subject != 'NO TIME (could not find stamp file)':
                    os.remove(stamp_file)
            del msg
        except smtplib.SMTPServerDisconnected:
            del msg
            f = open("ERROR_LOG.txt","a+")
            f.write('Error: Could not send some pictures.\n')
            f.write('\tDate: '+ datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n')
            f.write('\tConnected to Internet: ' + str(have_internet()) + '\n')
            f.close()
            return False
    return True
        
if __name__ == '__main__':
    receiver = 'Berginreceiver@gmail.com'

    #GMAIL TO GMAIL EXCHANGE
    #host_address = "aspmx.l.google.com"
    #port_number = 25

    #GMAIL TO GENERAL EXCHANGE (SMTP TLS)
    host_address = "smtp.gmail.com"
    port_number = 587

    path = "berginSenderCredentials.json"

    username, password, success = getCredentials(path)

    if success:

        server = setupSMTP(host_address, port_number, username, password)
        to_send = os.listdir('angle')
        to_send = ['angle/'+file_name for file_name in to_send]
           sent_all = sendAll(username, receiver, to_send, server, delete_sent = False)
        
        print("It is {} that all pictures were sent".format(str(sent_all)))
        server.quit()
