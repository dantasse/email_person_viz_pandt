#!/usr/bin/env python
#
# Script to read from a directory of processed emails, and output word
# counts of each message per person. There's some good stuff to reuse here
# and some one-off stuff. The output of this was a chart posted to our room's
# bulletin board.
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

# TODO: this is not yet perfect. Some emails, particularly long ones, have some
# of the reply lines not starting with >'s, due to long line wrapping or
# something. What is this, the third century? Sigh. 
def is_reply(line):
    line = line.strip()
    if line.startswith('>'):
        return True
    elif line.startswith('On') and line.endswith('wrote:'):
        return True
    elif line.startswith('Nikola Banovic <nikola@dgp.toronto.edu> wrote:'):
        return True # I guess Toronto webmail mangles messages
    elif line.startswith('------') and 'Forwarded message' in line:
        return True
    elif line.startswith('------') and 'Original Message' in line:
        return True
    else:
        return False

word_counts = {'Brandon': [], 'Nikola': [], 'Dave': [], 'Chris': [], 'Tati': [],\
               'Jenny': [], 'Anthony': []}

# Returns a set of lines with all the reply ones removed.
# This is not perfect too. It's heuristics, you can see.
# Particularly, it fails if someone replies inline. I think that's rarer in
# this dataset than long mangled emails.
def remove_replies(msg_lines):
    good_lines = []
    for line in msg_lines:
        if is_reply(line):
            return good_lines
        else:
            good_lines.append(line)
    return good_lines

def get_word_counts(filepath):
    file = open(filepath, 'r')
    contents = file.readlines()
    from_address = contents[1].strip()
    for person in people:
        if from_address in people[person]:
            msg_lines = contents[4:]
            #msg_lines_noreplies = [line for line in msg_lines if not is_reply(line)]
            msg_lines_noreplies = remove_replies(msg_lines)
            words = ''.join(msg_lines_noreplies).split()
            word_counts[person].append(len(words))
            if len(words) > 250:
                print "long file. length = " + str(len(words)) + " " +  filepath
   
for filename in os.listdir(cmu_path):
    get_word_counts(cmu_path + filename)
for filename in os.listdir(gmail_path):
    get_word_counts(gmail_path + filename)

print word_counts
for person in word_counts:
    print person
    print word_counts[person]

