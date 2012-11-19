#!/usr/bin/env python
#
# Script to get a few "meaningful" snippets out of email, given a person.
#
# Each email should be in the form:
"""
date/time (UTC)
from address
to addresses
cc addresses
rest of the text
"""

import argparse, datetime, os, random
import email_lib

parser = argparse.ArgumentParser(description='Display some "meaningful"\
    snippets, given email between you and another person.')
 
parser.add_argument('me',
    help='your email address')
parser.add_argument('person',
    help='the email address of the person you want to get snippets from')
parser.add_argument('--start_date',
    default='0001-01-01',
    help='the start date (inclusive) of the range you want to search, in\
          format YYYY-MM-DD')
parser.add_argument('--end_date',
    default='9999-12-30',
    help='the end date (inclusive) of the range you want to search, in format\
          YYYY-MM-DD')
parser.add_argument('-p', '--emails_path',
    default='/Users/dtasse/Desktop/processed_emails/',
    help='the path to the directory with all the emails')
parser.add_argument('-n', '--num_snippets', type=int, default=1,
    help='the number of snippets to get')

args = parser.parse_args()
start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d')
end_date = datetime.datetime.strptime(args.end_date, '%Y-%m-%d')\
    + datetime.timedelta(days=1)
# Adding a day to facilitate comparisons. This is creating a date at 00:00:00,
# so if end date is May 3, let's compare to the first second of May 4, not the
# first second of May 3.

class email:
    """ represents an email """
    def __init__(self, date, from_address, to_addresses, cc_addresses, text):
        self.date = date
        self.from_address = from_address
        self.to_addresses = to_addresses
        self.cc_addresses = cc_addresses
        self.text = text

def read_email(filepath):
    file = open(filepath, 'r')
    contents = file.readlines()
    date_string = contents[0].strip()
    #TODO: I never specified that the string should be in this format when
    # it is written to the file in the first place. I should do that.
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    from_address = contents[1].strip()
    # note that we expect to_addresses to be safe
    to_addresses = eval(contents[2].strip())
    cc_addresses = eval(contents[3].strip())
    msg_lines = contents[4:]
    msg_lines_noreplies = email_lib.remove_replies(msg_lines)
    msg_text = ''.join(msg_lines_noreplies)

    return email(date, from_address, to_addresses, cc_addresses, msg_text)
 
def is_email_good(email):
    is_right_people =\
        (args.person == email.from_address and args.me in email.to_addresses) or\
        (args.person in email.to_addresses and args.me == email.from_address)
    # TODO Off by ~5 hrs due to timezones. Don't care for now, but would
    # be nice to fix someday.
    is_date_okay = email.date >= start_date and email.date <= end_date
    return is_right_people and is_date_okay

count = 0
for filename in os.listdir(args.emails_path):
    e1 = read_email(args.emails_path + filename)
    if is_email_good(e1):
        count += 1
print count

