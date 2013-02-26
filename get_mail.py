#!/usr/bin/env python
#
# Script to get all your email from gmail.
# For my 62k emails, it took about 6-7 hrs (twice) on 12/6/12.
# For Daniel's 15k emails, it took about 80 minutes.
# For my 3k emails from work, took 10 minutes.
#
# From this Stack Overflow post:
# http://stackoverflow.com/questions/348630/how-can-i-download-all-emails-with-attachments-from-gmail
# and
# https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/

import argparse, email, getpass, imaplib, os, time
from multiprocessing import Process

parser = argparse.ArgumentParser(description='Downloads all your email.')
parser.add_argument('path', help='Directory to save all your emails to.\
                                  Ending with a /')
args = parser.parse_args()

detach_dir = '.' # directory where to save attachments (default: current)
print "This application will attempt to save all your gmail to files.\
 If this is not what you want, quit now with ctrl-c." 
user = raw_input("Enter your GMail username:")
pwd = getpass.getpass("Enter your password: ")

# connecting to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(user,pwd)
m.select("[Gmail]/All Mail", readonly=True) # here you a can choose a mail box like INBOX instead
# use m.list() to get all the mailboxes

resp, items = m.search(None, "ALL") # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
items = items[0].split() # getting the mails id
print "Number of emails to download: " + str(len(items))

m2 = imaplib.IMAP4_SSL("imap.gmail.com")
m2.login(user,pwd)
m2.select("[Gmail]/All Mail", readonly=True) # do I have to do this again?


def get_one_email(mail_conn, id):
    resp, data = mail_conn.fetch(id, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
    email_body = data[0][1]
    output_file = open(args.path + 'email_' + str(id) + '.txt', 'w')
    output_file.write(email_body)
    output_file.close()

def get_some_emails(mail_conn, ids):
    for id in ids:
        get_one_email(mail_conn, id)

p2 = Process(target=get_some_emails, args=(m2, items[30000:]))
p2.start()

# TODO: split up evenly among processes, show some timing displays
get_some_emails(m, items[0:30000])


# start_time = time.time()
# emails_processed = 0
# for i in items[30000:40000]:
#     get_one_email(i)
#     emails_processed += 1
#     if (emails_processed % 100 == 0):
#         print 'This many messages downloaded: ' + str(emails_processed)
#         num_sec = time.time() - start_time
#         print 'This many seconds: ' + str(num_sec)
#         rate = emails_processed / num_sec
#         print 'Rate: ' + str(rate) + ' messages per second'
#         est_sec_left = (len(items) - emails_processed) / rate
#         print 'Estimated minutes left: ' + str(est_sec_left / 60)
