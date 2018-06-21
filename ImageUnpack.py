#some code adapted from: https://gist.github.com/xiconet/effbe998d4708b96757f

import email
import getpass, imaplib
import os
import sys

from PYemail import getCredentials

def unpack(username, password, saveFolder, sender_email = 'berginsender@gmail.com'):
	'''
	Saves pictures and timestamps in emails from sender_email to a local
	folder
	
	Parameters
	username: username for the email account
	password: password for the email account
	saveFolder: the desired folder to which attachments will be saved 
		(will be created if it is nonexistent)
	sender_email: the exclusive email from which we should download attachments
	'''
	detach_dir = '.'
	if saveFolder not in os.listdir(detach_dir):
		os.mkdir(saveFolder)

	imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
	typ, accountDetails = imapSession.login(username, password)
	if typ != 'OK':
		print('Not able to sign in!')
		sys.exit()

	imapSession.select('"[Gmail]/All Mail"')
	typ, data = imapSession.search(None, '(FROM "{}")'.format(sender_email))
	if typ != 'OK':
		print('Error searching Inbox.')
		sys.exit()

	# Iterating over all emails
	for msgId in data[0].split():
		print('msgId: {}'.format(msgId))
		typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
		if typ != 'OK':
			print('Error fetching mail.')
			continue

		emailBody = messageParts[0][1]
	
		mail = email.message_from_bytes(emailBody)
		subject = mail['subject']
		for part in mail.walk():
			if part.get('Content-Disposition') is None:
				continue
		
			file_exists = part.get('Content-Disposition').startswith('attachment')
			fileName = part.get_filename()
			print(fileName)
		
			if bool(file_exists):
				#let the new file name include the time
				fileName = subject + "_" + fileName 
				filePath = os.path.join(detach_dir, saveFolder, fileName)
				fp = open(filePath, 'wb')
				fp.write(part.get_payload(decode=True))
				fp.close()
		imapSession.store(msgId, '+X-GM-LABELS', '\\Trash')
	imapSession.select('[Gmail]/Trash')
	imapSession.store('1:*','+FLAGS','\\Deleted')
	print(imapSession.expunge())
	imapSession.close()
	imapSession.logout()

if __name__ == '__main__':
	saveFolder = 'attachments'
	path = "../Credentials/berginRecieverCredentials.json"
	username, password, success = getCredentials(path)
	if success:
		unpack(username, password, saveFolder)
	else:
		print('Could not find credentials')
