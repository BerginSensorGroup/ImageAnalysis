#some code adapted from: https://gist.github.com/xiconet/effbe998d4708b96757f

import email
import getpass, imaplib
import os
import sys

from PYemail import getCredentials

if __name__ == '__main__':

	detach_dir = '.'
	if 'attachments' not in os.listdir(detach_dir):
		os.mkdir('attachments')

	path = "../Credentials/berginRecieverCredentials.json"
	senderPath = "../Credentials/berginSenderCredentials.json"
	host_address = "smtp.gmail.com"
	port_number = 587
	userName, passwd, success = getCredentials(path)


	imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
	typ, accountDetails = imapSession.login(userName, passwd)
	if typ != 'OK':
		print('Not able to sign in!')
		sys.exit()

	imapSession.select('"[Gmail]/All Mail"')
	typ, data = imapSession.search(None, '(UNSEEN)')
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
			print('\tLooking at a part of this message')
		
			if part.get('Content-Disposition') is None:
				print('\t\tContent-Disposition is none')
				continue
		
			print('\t\t'+str(part.get('Content-Disposition').startswith('attachment')))
			file_exists = part.get('Content-Disposition').startswith('attachment')
			fileName = part.get_filename()
			print(fileName)
		
			if bool(file_exists):
				#let the new file name include the time
				fileName = subject + "_" + fileName 
				filePath = os.path.join(detach_dir, 'attachments', fileName)
				print(fileName)
				fp = open(filePath, 'wb')
				fp.write(part.get_payload(decode=True))
				fp.close()
		print("Will delete " + 'msgId: {}'.format(msgId))
		print(imapSession.store(msgId, '+X-GM-LABELS', '\\Trash'))
	print('deleting now')
	imapSession.select('[Gmail]/Trash')
	imapSession.store('1:*','+FLAGS','\\Deleted')
	print(imapSession.expunge())
	imapSession.close()
	imapSession.logout()

