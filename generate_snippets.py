#!/usr/bin/env python
#
# Script to get a few "meaningful" snippets out of email, given a person.
"""
date/time (UTC)
from address
to addresses
cc addresses
rest of the text
"""

import argparse, datetime, os, pickle, random, re, string, sys
import email_lib, tfidf

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
parser.add_argument('--snippet_chars', type=int, default=400,
    help='the approximate number of characters in each snippet')
parser.add_argument('--use_keyword', action='store_true',
    help='if set, use keyword matching (like "love") to find snippets')
parser.add_argument('--use_tfidf', action='store_true',
    help='if set, use TF-IDF algorithm to pick snippets based on words that ' +
         'you use with that person more than most people')
parser.add_argument('--use_all_caps', action='store_true',
    help='if set, pick snippets that have a word in all caps.')

args = parser.parse_args()

if not (args.use_keyword or args.use_tfidf or args.use_all_caps):
    sys.exit("You must set at least one way to find snippets. " +\
             "Try ./generate_snippets -h for details.")

start_date = datetime.datetime.strptime(args.start_date, email_lib.DATE_FORMAT)
end_date = datetime.datetime.strptime(args.end_date, email_lib.DATE_FORMAT)\
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

segmenter_file = open('english.pickle', 'r')
sentence_segmenter = pickle.Unpickler(segmenter_file).load()
# Another way to get the sentence_segmenter (and probably more official) is to
# download it from nltk's data downloader (nltk.org/data.html), and then call:
# sentence_segmenter = nltk.data.load('tokenizers/punkt/english.pickle')


if args.use_tfidf:
    tfidf_words = [word_score[0] for word_score in\
        tfidf.get_unusual_words(args.emails_path, args.me, args.person)[0:12]]
    for word in tfidf_words:
        print word

# build it out until it's approx snippet_chars length
# |sentences| = all sentences in the email, |index| = index of matching word
def build_long_snippet(sentences, index):
    max_length = 1.2 * args.snippet_chars
    long_snippet = sentences[index]
    start_index = index # index of matching word
    end_index = index + 1
    while len(long_snippet) < args.snippet_chars:
        if end_index < len(sentences):
            end_index += 1
        new_long_snippet = ' '.join(sentences[start_index:end_index])
        if len(new_long_snippet) > max_length:
            return long_snippet
        long_snippet = new_long_snippet

        if start_index > 0:
            start_index -= 1
        new_long_snippet = ' '.join(sentences[start_index:end_index])
        if len(new_long_snippet) > max_length:
            return long_snippet

        if start_index <= 0 and end_index >= len(sentences):
            return new_long_snippet
        long_snippet = new_long_snippet

    return long_snippet

def remove_links(text):
    return re.sub('http://\S*', '(link)', text)
 
key_words = [':)', ':-)', 'lol', 'love', 'i feel', 'xoxo', 'haha']
# Returns a list of snippets, as defined in email_lib (a "snippet" is a
# potentially-meaningful sentence).
def get_snippets(email):
    snippets = []
    text_no_newlines = remove_trn(email.text)
    text_no_links = remove_links(text_no_newlines)
    sentences = sentence_segmenter.tokenize(text_no_links)
    for index, sentence in enumerate(sentences):
        sentence_good = False
        reasons = [] # reasons that sentence is good
        if args.use_keyword:
            for key_word in key_words:
                if key_word in sentence.lower().split():
                    sentence_good = True
                    reasons.append('key word: ' + key_word)
        if args.use_tfidf:
            for tfidf_word in tfidf_words:
                if tfidf_word in [word.strip(string.punctuation) for word in\
                    sentence.lower().split()[0:-1]]:
                    sentence_good = True
                    reasons.append('tfidf: ' + tfidf_word)
        if args.use_all_caps:
            for word in sentence.split():
                # all caps: word length >3 to avoid junk and acronyms
                if len(word.strip(string.punctuation + string.digits)) > 3\
                    and word.isupper():
                    sentence_good = True
                    reasons.append('all caps: ' + word)
        if sentence_good:
            long_snippet = build_long_snippet(sentences, index)
            snippet = email_lib.snippet(sentence, email.from_address,\
                email.text, long_snippet, reasons)
            snippets.append(snippet)
            
    return snippets
 
all_snippets = []
for filename in os.listdir(args.emails_path):
    e1 = email_lib.read_email(args.emails_path + filename)
    if is_email_valid(e1):
        for snippet in get_snippets(e1):
            snippet.filename = filename
            all_snippets.append(snippet)

for snippet in all_snippets:
    print snippet.filename
    print snippet.long_snippet
    print ','.join(snippet.reasons)
    print

if len(all_snippets) == 0:
    print "No snippets." 
