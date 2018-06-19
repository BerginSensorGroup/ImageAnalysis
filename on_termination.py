import PYemail
import sys
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
	
	credentials_path = "../Credentials/berginSenderCredentials.json"
	#GMAIL TO GENERAL EXCHANGE (SMTP TLS)
	host_address = "smtp.gmail.com"
	port_number = 587
	
	username, password, success = PYemail.getCredentials(credentials_path)
	if not success:
		#this program is useless without an email account to send the warning
		sys.exit()
	while not PYemail.have_internet():
		pass
	server = PYemail.setupSMTP(host_address, port_number, username, password)
	
	for warning_receiver in warning_receivers:
		msg = PYemail.formatMessage(username, warning_receiver, [], subject = "Warning for {}: master.py terminated and will not resume".format(name))
		server.send_message(msg)
