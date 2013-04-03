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
parser.add_argument('top_emailers',
    help='the email address of the person you want to get snippets from',
    nargs='*')
parser.add_argument('--start_date',
    default='0001-01-01',
    help='the start date (inclusive) of the range you want to search, in\
          format YYYY-MM-DD')
parser.add_argument('--end_date',
    default='9999-12-30',
    help='the end date (inclusive) of the range you want to search, in format\
          YYYY-MM-DD')
parser.add_argument('-p', '--emails_path',
    help='the path to the directory with all the emails')
parser.add_argument('-n', '--num_snippets', type=int, default=3,
    help='the number of snippets to get (per top emailer)')
parser.add_argument('--snippet_chars', type=int, default=400,
    help='the approximate number of characters in each snippet')
parser.add_argument('--use_keyword', default=True,
    help='if set, use keyword matching (like "love") to find snippets')
parser.add_argument('--use_tfidf', default=True,
    help='if set, use TF-IDF algorithm to pick snippets based on words that ' +
         'you use with that person more than most people')
parser.add_argument('--use_all_caps', default=True,
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
# (if it is between the right people, and if the date is okay)
def is_email_valid(email, me, top_emailer):
    is_right_people =\
        (top_emailer == email.from_address and me in email.to_addresses) or\
        (top_emailer in email.to_addresses and me == email.from_address)
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


tfidf_words={}
if args.use_tfidf:
    for top_emailer in args.top_emailers:
        tfidf_words[top_emailer] = [word_score[0] for word_score in\
            tfidf.get_unusual_words(args.emails_path, args.me, top_emailer)[0:12]]
        # print 'Unusual words with ' + top_emailer
        # for word in tfidf_words[top_emailer]:
        #     print word
        # print 

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
# You have to tell it who the email is with, so that it knows the right
# TFIDF (statistically unlikely) words for that person.
def get_snippets(email, top_emailer):
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
            for tfidf_word in tfidf_words[top_emailer]:
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
            snippet = email_lib.snippet(sentence, email.date, email.from_address,\
                email.to_addresses, email.text, long_snippet, reasons)
            snippets.append(snippet)
            
    return snippets
 
# returns N snippets from a particular top_emailer
def get_snippets_from_person(me, top_emailer):
    all_snippets_from_person = []
    for filename in os.listdir(args.emails_path):
        e1 = email_lib.read_email(args.emails_path + filename)
        if is_email_valid(e1, me, top_emailer):
            for snippet in get_snippets(e1, top_emailer):
                snippet.filename = filename
                all_snippets_from_person.append(snippet)

    # Randomly select N snippets
    random.shuffle(all_snippets_from_person)
    if args.num_snippets <= len(all_snippets_from_person):
        some_snippets = all_snippets_from_person[0:args.num_snippets]
    else:
        print "Not enough snippets."
        some_snippets = all_snippets_from_person
    return some_snippets

if __name__ == '__main__':
    all_snippets = []
    for top_emailer in args.top_emailers:
        snippets_from_person = get_snippets_from_person(args.me, top_emailer)
        if len(snippets_from_person) < args.num_snippets:
            print 'Warning: only %d snippets from %s' % (len(snippets_from_person), top_emailer)
        all_snippets.extend(snippets_from_person)

    random.shuffle(all_snippets)
    for snippet in all_snippets:
        print snippet.filename
        print 'From: ' + str(snippet.from_address)
        print 'To: ' + str(snippet.to_addresses)
        print str(snippet.date.date())
        print snippet.long_snippet
        print ','.join(snippet.reasons)
        print

    if len(all_snippets) == 0:
        print "No snippets." 
