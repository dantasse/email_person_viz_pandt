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

# let's save them each to a file so we don't have to keep asking gmail
email_id = 0
start_time = time.time()
time_spent_network = 0
time_spent_fs = 0
for emailid in items:
    net_time_start = time.time()
    resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
    time_spent_network += (time.time() - net_time_start)
    fs_time_start = time.time()
    email_body = data[0][1]
    output_file = open(args.path + 'email_' + str(email_id) + '.txt', 'w')
    email_id += 1
    output_file.write(email_body)
    output_file.close()
    time_spent_fs += (time.time() - fs_time_start)
    if (email_id % 100 == 0):
        print 'This many messages downloaded: ' + str(email_id)
        num_sec = time.time() - start_time
        print 'This many seconds: ' + str(num_sec)
        rate = email_id / num_sec
        print 'Rate: ' + str(rate) + ' messages per second'
        est_sec_left = (len(items) - email_id) / rate
        print 'Estimated minutes left: ' + str(est_sec_left / 60)
        print 'Time spent over network: ' + str(time_spent_network)
        print 'Time spent in file system: ' + str(time_spent_fs)
