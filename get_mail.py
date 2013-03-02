#!/usr/bin/env python
#
# Script to get all your email from gmail.
#
# From this Stack Overflow post:
# http://stackoverflow.com/questions/348630/how-can-i-download-all-emails-with-attachments-from-gmail
# and
# https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/

import argparse, email, getpass, imaplib, os, time
from multiprocessing import Process, Value

parser = argparse.ArgumentParser(description='Downloads all your email.')
parser.add_argument('--path', help='Directory to save all your emails to.\
                                  Ending with a /', default='emails/')
parser.add_argument('--processes', help='How many workers to use.',
                    type=int, default=10)
args = parser.parse_args()

# create the output folder
directory = os.path.dirname(args.path)
if not os.path.exists(directory):
    os.makedirs(directory)

print "This application will attempt to save all your gmail to files.\
 If this is not what you want, quit now with ctrl-c." 
user = raw_input("Enter your GMail username:")
pwd = getpass.getpass("Enter your password: ")

# start and authenticate a new process for each worker
mail_conns = []
for i in range(args.processes):
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

def get_hundred_emails(mail_conn, ids):
    # TODO you can fetch a range of ids, I think! try getting multiple messages at once.
    # TODO get the odd corner cases after all the even hundreds
    resp, data = mail_conn.fetch(','.join(ids), "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
    # No sense in trying to get only the attachments, b/c gmail throttles us
    # after a certain number of requests anyway. blah.
    
    if resp != 'OK':
        print "Get " + str(id) + ": " + str(resp)

    for idx, val in enumerate(data):
        # This gives us a goofy two-part array that has all the even numbers
        # with one email message each and the odd numbers with just a close
        # paren. meh?
        if (idx % 2 == 0):
            # print val[1]
            
            email_body = val[1]
            output_file = open(args.path + 'email_' + str(ids[idx/2]) + '.txt', 'w')
            output_file.write(email_body)
            output_file.close()

def get_some_emails(mail_conn, ids, emails_gotten):
    while(len(ids) > 100):
        first_ten_ids = ids[0:100]
        ids = ids[100:]
        get_hundred_emails(mail_conn, first_ten_ids)
        emails_gotten.value += 100
        if (emails_gotten.value % 1000 == 0):
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

