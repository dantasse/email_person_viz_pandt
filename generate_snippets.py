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

parser = argparse.ArgumentParser(description='Display some "meaningful"\
    snippets, given email between you and another person.')
 
parser.add_argument('me',
    help='your email address')
parser.add_argument('person',
    help='the email address of the person you want to get snippets from')
parser.add_argument('--start_date',
    default='2012-10-01',
    help='the start date of the range you want to search, in format YYYY-MM-DD')
parser.add_argument('--end_date',
    default='2012-12-31',
    help='the end date of the range you want to search, in format YYYY-MM-DD')
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

# TODO: this is not yet perfect. Some emails, particularly long ones, have some
# of the reply lines not starting with >'s, due to long line wrapping or
# something. What is this, the third century? Sigh. 
# TODO factor out into library
def is_reply(line):
    line = line.strip()
    if line.startswith('>'):
        return True
    elif line.startswith('On') and line.endswith('wrote:'):
        return True
    elif line.startswith('------') and 'Forwarded message' in line:
        return True
    elif line.startswith('------') and 'Original Message' in line:
        return True
    else:
        return False

# Returns a set of lines with all the reply ones removed.
# This is not perfect too. It's heuristics, you can see.
# Particularly, it fails if someone replies inline. I think that's rarer in
# this dataset than long mangled emails.
# TODO factor out into library
def remove_replies(msg_lines):
    good_lines = []
    for line in msg_lines:
        if is_reply(line):
            return good_lines
        else:
            good_lines.append(line)
    return good_lines

def read_email(filepath):
    file = open(filepath, 'r')
    contents = file.readlines()
    from_address = contents[1].strip()
    # note that we expect to_addresses to be safe
    to_addresses = eval(contents[2].strip())
    date_string = contents[0].strip()
    #TODO: I never specified that the string should be in this format when
    # it is written to the file in the first place. I should do that.
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    if ((args.person == from_address and args.me in to_addresses) or\
        (args.person in to_addresses and args.me == from_address)) and\
        date >= start_date and date <= end_date:
        # TODO Off by ~5 hrs due to timezones. Don't care for now, but would
        # be nice to fix someday.
        msg_lines = contents[4:]
        msg_lines_noreplies = remove_replies(msg_lines)
        msg_text = ''.join(msg_lines_noreplies)
 
for filename in os.listdir(args.emails_path):
    read_email(args.emails_path + filename)

