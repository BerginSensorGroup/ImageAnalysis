import PYemail
import sys
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

if __name__ == '__main__':
	'''
	This program is intended to be executed following master.py
	
	As master.py has a while true loop, it will not halt unless
	something goes wrong.
	
	If that something is power loss or system crash then there is no big deal
	as master.py execution will resume upon reboot.
	
	If that something is an uncaught exception then the program will not
	continue executing later and we need to know that the sensor will not
	take data until it is serviced.
	'''
	#path of termination log, must be the same as in master.py
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
	
	#Who should recieve the warning emails?
	warning_receivers = ["xavier.boudreau@duke.edu", "jrf36@duke.edu"]
	
	send_credentials_folder = "../Credentials/sending_credentials/"
        
	credential_paths = os.listdir(send_credentials_folder)
	credential_paths = [send_credentials_folder + json_name for json_name in credential_paths]
	
	for credential_path in credential_paths:
		try:
			host_address, port_number, username, password, success = PYemail.getCredentials(credential_path)
			if not success:
				#we can only send the warning if we have a valid email
				continue
			while not PYemail.have_internet():
				pass
			server = PYemail.setupSMTP(host_address, port_number, username, password)
			
			for warning_receiver in warning_receivers:
				msg = PYemail.formatMessage(username, warning_receiver, [termination_log_path], subject = "Warning for {}: master.py terminated and will not resume".format(name))
				server.send_message(msg)
			#if we managed to send the warning then finish the program
			break
			
		except:
			#if we didn't manage to send the warning try again with the next account
			#print('refused')
			continue
