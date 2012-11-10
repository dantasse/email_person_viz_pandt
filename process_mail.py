#!/usr/bin/env python
#
# Grabs raw emails from a folder and turns them into a somewhat nicer format
# for further use.
#
# Some details from:
# https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/

import datetime, email, os

def remove_trn(s):
    return s.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

path = '/Users/dtasse/Desktop/emails/'

for filename in os.listdir(path):
    contents = open(path + filename, 'r').read()
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
        print "error parsing date: " + msg['date']

    print "%s\t%s\t%s\t%s" % (utc_date, from_addr, to_addrs, cc_addrs)

    # TODO get the actual message text
