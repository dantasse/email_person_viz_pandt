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
import nltk.data
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

# Returns whether the email should even be considered as a possible candidate
def is_email_valid(email):
    is_right_people =\
        (args.person == email.from_address and args.me in email.to_addresses) or\
        (args.person in email.to_addresses and args.me == email.from_address)
    # TODO Off by ~5 hrs due to timezones. Don't care for now, but would
    # be nice to fix someday.
    is_date_okay = email.date >= start_date and email.date <= end_date
    return is_right_people and is_date_okay

def remove_trn(s):                                                              
    return s.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

sentence_segmenter = nltk.data.load('tokenizers/punkt/english.pickle')
key_words = [':)', ':-)', 'lol', 'love', 'i feel', 'xoxo']
# Returns a list of string snippets (a "snippet" is a potentially-meaningful
# sentence). TODO maybe snippets should be >1 sentence.
def get_snippets(email):
    snippets = []
    text_no_newlines = remove_trn(email.text)
    sentences = sentence_segmenter.tokenize(text_no_newlines)
    for sentence in sentences:
        #TODO all we've got here is the keyword matcher, add more ways to pick
        # out snippets
        for key_word in key_words:
             if key_word in sentence.lower():
                 snippets.append(sentence)
    return snippets
 
for filename in os.listdir(args.emails_path):
    e1 = email_lib.read_email(args.emails_path + filename)
    if is_email_valid(e1):
        for snippet in get_snippets(e1):
            print snippet

