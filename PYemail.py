#some code altered from:
#https://stackoverflow.com/questions/3362600/how-to-send-email-attachments
#and
#https://medium.freecodecamp.org/send-emails-using-code-4fcea9df63f

import json
import smtplib
import os.path as op
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders


receiver = 'BerginReciever@gmail.com'

#GMAIL TO GMAIL EXCHANGE
#host_address = "aspmx.l.google.com"
#port_number = 25

#GMAIL TO GENERAL EXCHANGE (SMTP TLS)
host_address = "smtp.gmail.com"
port_number = 587

path = "berginSenderCredentials.json"

def setup(host_address, port_number, username, password):
	# set up the SMTP server
	s = smtplib.SMTP(host= host_address, port= port_number)
	s.starttls()
	s.login(username, password)
	return s

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
	except:
		return "","", False

def formatMessage(sender, reciever, subject, files):
	'''
	formats an email message to send by SMTP server
	
	Parameters
	sender: the email account sending the message
	reciever: the email account receiveing the message
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

username, password, success = getCredentials(path)

if success:

	server = setup(host_address, port_number, username, password)
	files = ['angle/G0011576.JPG', 'angle/G0011577.JPG']
	msg = formatMessage(username, receiver, 'success', files)
	

	# send the message via the server set up earlier.
	server.send_message(msg)
	del msg

	# Terminate the SMTP session and close the connection
	server.quit()