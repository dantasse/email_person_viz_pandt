#!/usr/bin/env python
#
# Script to read from a directory of processed emails, and output word
# counts of each message per person. There's some good stuff to reuse here
# and some one-off stuff. The output of this was a chart posted to the bulletin
# board outside our offices.
#
# Each email should be in the form:
"""
date/time (UTC)
from address
to addresses
cc addresses
rest of the text
"""

import os, random
import email_lib

cmu_path = "/Users/dantasse/Desktop/processed_emails/"
gmail_path = "/Users/dantasse/Desktop/dantasse_processed_emails/"


brandon_emails = ['taylor.brandon.t@gmail.com', 'bttaylor@andrew.cmu.edu']
nikola_emails = ['nikola.banovic@gmail.com', 'nikola@dgp.toronto.edu', 'nbanovic@cs.cmu.edu', 'nbanovic@andrew.cmu.edu']
dave_emails = ['dgerrits@andrew.cmu.edu', 'davidalso@gmail.com']
chris_emails = ['maclellan.christopher@gmail.com', 'cmaclell@cs.cmu.edu', 'cmaclell@andrew.cmu.edu']
tati_emails = ['tvlahovi@cs.cmu.edu', 'tavlahovic@gmail.com', 't.vlahovic4611@gmail.com', 'tvlahovi@andrew.cmu.edu']
jenny_emails = ['jenno0101@gmail.com', 'jkolsen@cs.cmu.edu', 'jkolsen@andrew.cmu.edu']
anthony_emails = ['xiangchen@acm.org', 'anthony.xiangchen@gmail.com', 'xiangchen@cmu.edu', 'xiangche@andrew.cmu.edu']

people = {'Brandon':brandon_emails, 'Nikola':nikola_emails, 'Dave': dave_emails,\
          'Chris':chris_emails, 'Tati':tati_emails, 'Jenny':jenny_emails,\
          'Anthony':anthony_emails}
word_counts = {'Brandon': [], 'Nikola': [], 'Dave': [], 'Chris': [], 'Tati': [],\
               'Jenny': [], 'Anthony': []}

# TODO if I ever use this again, refactor to use email_lib.read_email
def get_word_counts(filepath):
    file = open(filepath, 'r')
    contents = file.readlines()
    from_address = contents[1].strip()
    for person in people:
        if from_address in people[person]:
            msg_lines = contents[4:]
            msg_lines_noreplies = email_lib.remove_replies(msg_lines)
            words = ''.join(msg_lines_noreplies).split()
            word_counts[person].append(len(words))
            if len(words) > 250:
                print "long file. length = " + str(len(words)) + " " +  filepath
   
for filename in os.listdir(cmu_path):
    get_word_counts(cmu_path + filename)
for filename in os.listdir(gmail_path):
    get_word_counts(gmail_path + filename)

for person in word_counts:
    print person
    print word_counts[person]

