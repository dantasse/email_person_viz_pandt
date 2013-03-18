#!/usr/bin/env python
#
# Script to tell who are the people you email with most often.
# We will show this to our study participants, and they'll be able to pick
# which of those people they want to get postcards from.

import argparse, os
import email_lib
from collections import Counter

parser = argparse.ArgumentParser(description='Find the top N people that ' + \
    'you email most frequently.')
 
parser.add_argument('your_email', help='your email address')
parser.add_argument('-p', '--emails_path',
    default='processed_emails/',
    help='the path to the directory with all the emails')
parser.add_argument('-n', '--num_people', type=int, default=20,
    help='the number of people to get')
args = parser.parse_args()

top_people = Counter()
for filename in os.listdir(args.emails_path):
    e1 = email_lib.read_email(args.emails_path + filename)
    if args.your_email == e1.from_address:
        for to_address in e1.to_addresses:
            top_people[to_address] += 1
    # if you're in the from and the to, don't add yourself twice
    elif args.your_email in e1.to_addresses:
        top_people[e1.from_address] += 1

print top_people.most_common(args.num_people)

# Pretty-print top N
for person, count in top_people.most_common(args.num_people):
    print person + ', ' + str(count)



