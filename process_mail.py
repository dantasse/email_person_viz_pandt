#!/usr/bin/env python
#
# Grabs raw emails from a folder and turns them into a somewhat nicer format
# for further use.
# The output format is one file per email, in the format:
"""
Date
From address
To addresses
CC addresses 
Message text (all the rest of the lines too)
"""
#
# Some details from:
# https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/
#
# TODO should this just be combined with get_mail? Probably?

import argparse, datetime, email, os, time
import email_lib

parser = argparse.ArgumentParser(description='Processes your email to remove\
    all the extra garbage we don\'t need.')
parser.add_argument('raw_email_path', help='The directory where your emails\
    already are. (you should have run get_mail.py to put them there.')
parser.add_argument('output_path', help='The directory where you want to save\
    the processed emails to. (this directory should already exist as well.)')
args = parser.parse_args()


# path = '/Users/dtasse/Desktop/dantasse_emails/'
# outpath = '/Users/dtasse/Desktop/dantasse_processed_emails/'

def remove_trn(s):
    return s.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

# from yuji.wordpress.com address above
# TODO see the email I sent on Oct 29 at 3:58 PM to Tati, Nikola, Jenny.
# It has an attached Text file, which is garbled but gets parsed as another
# message.
def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()

heartbeat = 0
start_time = time.time()
for filename in os.listdir(args.raw_email_path):
    contents = open(args.raw_email_path + filename, 'r').read()
    msg = email.message_from_string(contents)
    
    from_str = remove_trn(msg['From'])
    from_addr = email.utils.parseaddr(from_str)[1]

    # getaddresses returns a list of ("Dan Tasse", "dantasse@cmu.edu") tuples
    tos = msg.get_all('to', [])
    to_addrs = [remove_trn(addr[1]).lower() for addr in email.utils.getaddresses(tos)]

    ccs = msg.get_all('cc', [])
    cc_addrs = [remove_trn(addr[1]).lower() for addr in email.utils.getaddresses(ccs)]

    date_tuple = email.utils.parsedate_tz(msg['date'])
    if date_tuple:
        utc_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
    else:
        print "error parsing date in file: " + filename
        continue

    text = get_first_text_block(msg)

    outfile = open(args.output_path + filename, 'w')
    outfile.write(utc_date.strftime(email_lib.DATE_TIME_FORMAT) + '\n')
    outfile.write(from_addr + '\n')
    outfile.write(str(to_addrs) + '\n')
    outfile.write(str(cc_addrs) + '\n')
    outfile.write(str(text))
    outfile.close()

    heartbeat += 1
    if (heartbeat % 1000 == 0):
        print "Messages processed: " + str(heartbeat)
    # print "%s\t%s\t%s\t%s" % (utc_date, from_addr, to_addrs, cc_addrs)

time_elapsed = time.time() - start_time
print "Done. Time elapsed: " + str(time_elapsed)
