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
from multiprocessing import Process, Value

parser = argparse.ArgumentParser(description='Downloads all your email.')
parser.add_argument('path', help='Directory to save all your emails to.\
                                  Ending with a /')
parser.add_argument('--processes', help='How many workers to use.',
                    type=int, default=1)
args = parser.parse_args()

detach_dir = '.' # directory where to save attachments (default: current)
print "This application will attempt to save all your gmail to files.\
 If this is not what you want, quit now with ctrl-c." 
user = raw_input("Enter your GMail username:")
pwd = getpass.getpass("Enter your password: ")

# start and authenticate a new process for each worker
mail_conns = []
for i in range(args.processes):
    print "starting a new process"
    # connecting to the gmail imap server
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login(user,pwd)
    m.select("[Gmail]/All Mail", readonly=True) # here you a can choose a mail box like INBOX instead
    # use m.list() to get all the mailboxes
    mail_conns.append(m)


resp, items = mail_conns[0].search(None, "ALL")
# you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
items = items[0].split() # getting the mails id
print "Number of emails to download: " + str(len(items))
start_time = time.time()

def get_one_email(mail_conn, id):
    resp, data = mail_conn.fetch(id, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
    email_body = data[0][1]
    output_file = open(args.path + 'email_' + str(id) + '.txt', 'w')
    output_file.write(email_body)
    output_file.close()

def get_some_emails(mail_conn, ids, emails_gotten):
    for id in ids:
        get_one_email(mail_conn, id)
        emails_gotten.value += 1
        if (emails_gotten.value % 100 == 0):
            print 'Emails saved:' + str(emails_gotten.value)
            elapsed_sec = time.time() - start_time
            print 'Time elapsed (seconds): ' + str(elapsed_sec)
            emails_left = len(items) - emails_gotten.value
            emails_per_minute = emails_gotten.value / elapsed_sec * 60
            print 'Expected time left (minutes): ' + str(emails_left / emails_per_minute)

# 7600 emails in 400 seconds, like 19 emails / sec
# started again at 5:51
if __name__ == '__main__':
    counter = Value('i', 0)
    num_emails = len(items)
    for i in range(len(mail_conns)):
        start_index = (num_emails * i) / len(mail_conns)
        end_index = (num_emails * (i+1)) / len(mail_conns)
        new_proc = Process(target=get_some_emails, args=(mail_conns[i],
                           items[start_index:end_index], counter))
        new_proc.start()

# TODO also error handling so one bad email doesn't kill the program

