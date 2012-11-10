#!/usr/bin/env python
#
# Grabs raw emails from a folder and turns them into a somewhat nicer format
# for further use.
#
# Some details from:
# https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/

import email, os

path = '/Users/dtasse/Desktop/emails/'

for filename in os.listdir(path):
  contents = open(path + filename, 'r').read()
  msg = email.message_from_string(contents)
  
  from_address = email.utils.parseaddr(msg['From'])[1]

  # getaddresses returns a list of ("Dan Tasse", "dantasse@cmu.edu") tuples
  tos = msg.get_all('to', [])
  to_addrs = [addr[1] for addr in email.utils.getaddresses(tos)]

  ccs = msg.get_all('cc', [])
  cc_addrs = [addr[1] for addr in email.utils.getaddresses(ccs)]

