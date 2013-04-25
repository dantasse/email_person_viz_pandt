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

import argparse, datetime, email, os, quopri, re, time
from multiprocessing import Pool, Value
import email_lib

parser = argparse.ArgumentParser(description='Processes your email to remove\
    all the extra garbage we don\'t need.')
parser.add_argument('--raw_email_path', help='The directory where your emails\
    already are. (you should have run get_mail.py to put them there.',
    default='emails/')
parser.add_argument('--output_path', help='The directory where you want to save\
    the processed emails to.',
    default='processed_emails/')
args = parser.parse_args()

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


global counter # sorry
counter = Value('i', 0)

def process_email(filename):
    try:
        contents = open(args.raw_email_path + filename, 'r').read()
        msg = email.message_from_string(contents)
        
        from_str = remove_trn(msg['From'] or '')
        from_addr = email.utils.parseaddr(from_str)[1].lower()

        # getaddresses returns a list of ("Dan Tasse", "dantasse@cmu.edu") tuples
        tos = msg.get_all('to', [])
        to_addrs = [remove_trn(addr[1]).lower() for addr in email.utils.getaddresses(tos)]

        ccs = msg.get_all('cc', [])
        cc_addrs = [remove_trn(addr[1]).lower() for addr in email.utils.getaddresses(ccs)]

        date_tuple = email.utils.parsedate_tz(msg['date'])
        if date_tuple:
            utc_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        else:
            print "could not parse date in file: " + filename + ", skipping file."
            return

        # TODO get the subject line

        text = get_first_text_block(msg)
        text = quopri.decodestring(str(text)) # fixes "=20" etc
        text = text.replace('\x92', "'") # there's some base64-encoded nonsense
        # going on here, I think, or windows-1252 or something. bug whack-a-mole?
        # maybe.
        text = text.replace('\x93', "'")
        text = text.replace('\xb2', '"')
        text = text.replace('\xb3', "'")
        text = text.replace('\xb4', "'")
        text = text.replace('\xb9', "'")
        text = text.replace('\xb36', '"')
        # text = re.sub('<.*?>', '', text) # Strip out everything in brackets
        text = re.sub('<http:.*>', '', text) # Strip out links

        outfile = open(args.output_path + filename, 'w')
        outfile.write(utc_date.strftime(email_lib.DATE_TIME_FORMAT) + '\n')
        outfile.write(from_addr + '\n')
        outfile.write(str(to_addrs) + '\n')
        outfile.write(str(cc_addrs) + '\n')
        outfile.write(text)
        outfile.close()

        global counter # sorry again
        counter.value += 1
        if (counter.value % 1000 == 0):
            print "emails processed: " + str(counter.value)
    except:
        print "Error on email: " + str(filename)
        

if __name__ == '__main__':

    # make sure the output directory exists
    outdir = os.path.dirname(args.output_path)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    print "Processing emails from " + str(args.raw_email_path) + ". Output will go to " + str(outdir) + "."

    start_time = time.time()
    p = Pool(10)
    files = os.listdir(args.raw_email_path)
    print "Number of emails to process: " + str(len(files))
    p.map(process_email, files)
    
    time_elapsed = time.time() - start_time
    print "Processing messages done. Time elapsed (seconds): " + str(time_elapsed)
