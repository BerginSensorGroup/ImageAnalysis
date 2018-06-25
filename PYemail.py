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


class credential_set(object):
    def __init__(self):
        self.credentials = []
        self.current = 0
    def addCredential(self, host_address, port_number, username, password):
        #time_expired will represent the time when the credentials were last refused
        minDateTime = datetime.datetime(1, 1, 1, 0, 0, 0, 0)
        self.credentials.append({'host address': host_address, 'port number': port_number, 
              'username': username, 'password': password, 'time expired': minDateTime})
    def updateExpiration(self, new_expiration = datetime.datetime.now()):
        self.credentials[self.current]['time expired'] = new_expiration
        self.current += 1
        if self.current >= len(self.credentials):
            self.current = 0
        return getCurrentCredentials(self)
    def getCurrentCredentials(self):
        if len(self.credentials) == 0:
            return None
        return (self.credentials[self.current]['host address'],
        			self.credentials[self.current]['port number'],
        			self.credentials[self.current]['username'], 
        			self.credentials[self.current]['password'])
        
        
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
        f.write('Error: Could not setup SMTP connection, will retry in a minute\n')
        return None

def getCredentials(path):
    '''
    Extracts and returns the host address, port number, username and password from a json in a tuple
    final value in tuple is True if success and False if failure
    
    It is optional for the json to have the host address and port number
        
    Parameters
    path: the path of the json to be read
    '''
    try:
        json_file = open(path, 'r')
        json_str = json_file.read()
        json_data = json.loads(json_str)
        return json_data["host address"], json_data["port number"], json_data["username"], json_data["password"], True
    except KeyError:
        #this json doesn't have host address and port number
        return json_data["username"], json_data["password"], True
    except IOError:
        #could not read the json
        f = open("ERROR_LOG.txt","a+")
        f.write('Error: JSON path was invalid.\n')
        f.close()
        return "","", False

def formatMessage(sender, receiver, files, subject = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"), failed_files = []):
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
        try:
            with open(path, 'rb') as file:
                part = MIMEBase('application', "octet-stream")
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition','attachment; filename="{}"'.format(op.basename(path)))
                msg.attach(part)
        except IOError:
            failed_files.append(path)
            f = open("ERROR_LOG.txt","a+")
            f.write('Error: lost file at: '+path+'\n')
            f.close()
    
    return msg

def get_stamp_and_stamp_path(stamp_paths, file_path):
    '''
    Given the file path, finds the corressponding time stamp in the provided stamp_paths list
    Assumes that each stamp_path ends in /<NUMBER>.ext where <NUMBER> is the desired stamp file number
    Assumes that the file path ends in /<TEXT>_<NUMBER>.ext where <NUMBER> is the desired stamp file number
    '''
    
    for stamp_path in stamp_paths:
        ext_loc = stamp_path.find('.')
        #the ID number will be after the final '/'
        last_slash = stamp_path.rfind('/')
        stamp_number = int(stamp_path[last_slash+1:ext_loc])
        
        ext_loc = file_path.find('.')
        #the ID number will be after the final '_'
        last_slash = file_path.rfind('_')
        file_number = int(file_path[last_slash+1:ext_loc])
        
        if stamp_number == file_number:
            with open(stamp_path, 'r') as f:
                return (f.read(), stamp_path)
    
    return ('NO TIME (could not find stamp file)', 'THIS_IS_NOT_A_FILE_PATH')

def sendAll(sender, receiver, file_paths, stamp_paths, server, delete_sent = True):
    '''
    Attempts to send all files located at the paths in file_paths via email
    
    sender: the email account sending the message
    receiver: the email account receiveing the message
    file_paths: a list of (str) paths to jpg files that need to be sent
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
                    os.remove(stamp_path)
            del msg
        except smtplib.SMTPServerDisconnected:
            del msg
            f = open("ERROR_LOG.txt","a+")
            f.write('Error: Could not send some pictures due to disconnected SMTP.\n')
            f.write('\tDate: '+ datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n')
            f.write('\tConnected to Internet: ' + str(have_internet()) + '\n')
            f.close()
            return False
    return True

def sendAllJson(sender, receiver, json_paths, server, delete_sent = True):
    '''
    Attempts to send all files located at the paths in file_paths via email
    
    sender: the email account sending the message
    receiver: the email account receiveing the message
    json_paths: a list of (str) paths to json files that need to be sent
        the json files should hold an entry of:
            "taken": "<TIME>" where <TIME> is time the pictures were taken (will be subject line)
        the json files should hold an entry array of:
            "picture_paths": ["<SOME_PATH.jpg>", "<SOME_PATH2.jpg>", ...]
        All pictures found at the paths in this array will be sent in one email
        For this reason it is important that the array not be filled with more bytes
        than the maximum one email can send
    '''
    for json_path in json_paths:
        json_file = open(json_path)
        json_str = json_file.read()
        picture_data = json.loads(json_str)
        failed_files = []
        msg = formatMessage(sender, receiver, picture_data["picture_paths"], picture_data["taken"], failed_files)
        try:
            server.send_message(msg)
            if delete_sent:
                for picture_path in picture_data["picture_paths"]:
                    if picture_path not in failed_files:
                        os.remove(picture_path)
                os.remove(json_path)
            del msg
        except smtplib.SMTPServerDisconnected:
            #this exception likely happened because we lost internet before we could send the message
            del msg
            f = open("ERROR_LOG.txt","a+")
            f.write('Error: Could not send some pictures due to disconnected SMTP.\n')
            f.write('\tDate: '+ datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n')
            f.write('\tConnected to Internet: ' + str(have_internet()) + '\n')
            f.close()
            return False
            
    return True
