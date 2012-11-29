#!/usr/bin/env python
#
# Finds words that are more common between |you| and |target person| than
# between you and other people.
#
# doc_frequencies = {"word" : num_people_you_say_this_word_with}
# alternately, doc_frequencies = {"word" : total number of times word appears}
# term_frequency = {"word" : counts in emails with you and friend}

from collections import defaultdict
import os, string
import email_lib

# returns a list of email objects, defined in email_lib
def read_all_files(path):
    emails = []
    for filename in os.listdir(path):
        emails.append(email_lib.read_email(path + filename))
    return emails

def remove_trn(s):                                                              
    return s.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

# removes punctuation from the start and end of a string
def remove_punct(s):
    return s.strip(string.punctuation)

# some words are okay to have in emails but are definitely not meaningful.
# for example: "http://www.google.com".
def is_valid_tfidf_word(word):
    if len(word) > 50:
        return False
    elif word.startswith('http'):
        return False
    else:
        return True

def normalize_word(word):
    return remove_punct(word.lower())

# returns a map of {email_address: list of texts of emails between
# |your_address| and that person}
def texts_by_person(emails, your_address):
    person_emails = defaultdict(list)
    for email in emails:
        if email.from_address == your_address:
            for to_address in email.to_addresses:
                person_emails[to_address].append(remove_trn(email.text))
        elif your_address in email.to_addresses:
            person_emails[email.from_address].append(remove_trn(email.text))
    return person_emails

# returns a map of {word: number of people you say word with}
# all words in lowercase
def get_doc_frequencies(person_email_texts):
    doc_frequencies = defaultdict(int)
    for person in person_email_texts:
        emails = ' '.join(person_email_texts[person])
        # emails.split() is all the words this person has said
        for word in set(emails.split()):
            if is_valid_tfidf_word(word):
                doc_frequencies[normalize_word(word)] += 1
    return doc_frequencies


# |emails_path| is the path to all the email files.
# |you| is your email address, |other| is the other person's
# returns a list of (word, tfidf score) tuples, sorted by score, highest first
def get_unusual_words(emails_path, you, other):
    emails = read_all_files(emails_path)
    person_email_texts = texts_by_person(emails, you)
    doc_frequencies = get_doc_frequencies(person_email_texts)
    term_frequencies = defaultdict(int)
    for email in person_email_texts[other]:
        for word in email.split():
            if is_valid_tfidf_word(word):
                term_frequencies[normalize_word(word)] += 1
    tfidf = {}
    for word in term_frequencies:
        tfidf[word] = term_frequencies[word] * 1.0 / doc_frequencies[word]
    retval = sorted(tfidf.items(), key=lambda x: x[1])
    # print retval
    retval.reverse()
    return retval

