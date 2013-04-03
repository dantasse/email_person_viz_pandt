#!/usr/bin/env python
#
# Functions that may be useful as we deal with emails a bunch.
#
import datetime, string

DATE_FORMAT = '%Y-%m-%d'
DATE_TIME_FORMAT = DATE_FORMAT + ' %H:%M:%S'

class email:
    """ represents an email """
    def __init__(self, date, from_address, to_addresses, cc_addresses, text):
        self.date = date
        self.from_address = from_address
        self.to_addresses = to_addresses
        self.cc_addresses = cc_addresses
        self.text = text

class snippet:
    """ represents a hopefully-meaningful snippet of text and the email that
        it is in.
        snippet = the "meaningful" sentence
        from_address: who wrote it
        to_addresses: who it's to
        email_text: the full text of the email
        long_snippet: a longer (3 sentences) version of the "meaningful" snippet
        reasons: why is it a good sentence?
        filename: the file name it's saved as (optional, for debugging)
    """
    def __init__(self, snippet, date, from_address, to_addresses, email_text, long_snippet, reasons):
        self.snippet = snippet
        self.date = date
        self.from_address = from_address
        self.to_addresses = to_addresses
        self.email_text = email_text
        self.long_snippet = long_snippet
        self.reasons = reasons
    filename = ''

# TODO: this is not yet perfect. Some emails, particularly long ones, have some
# of the reply lines not starting with >'s, due to long line wrapping or
# something. What is this, the third century? Sigh. 
def is_reply(line):
    line = line.strip()
    if line.startswith('>'):
        return True
    elif line.startswith('On') and line.endswith('wrote:'):
        return True
    elif line.startswith('--') and 'forwarded message' in line.lower():
        return True
    elif line.startswith('--') and 'original message' in line.lower():
        return True
    else:
        return False

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


def read_email(filepath):
    file = open(filepath, 'r')
    contents = file.readlines()
    date_string = contents[0].strip()
    date = datetime.datetime.strptime(date_string, DATE_TIME_FORMAT)
    from_address = contents[1].strip()
    # note that we are calling eval; we expect to_addresses to be safe
    to_addresses = eval(contents[2].strip())
    cc_addresses = eval(contents[3].strip())
    msg_lines = contents[4:]
    msg_lines_noreplies = remove_replies(msg_lines)
    msg_text = ''.join(msg_lines_noreplies)

    return email(date, from_address, to_addresses, cc_addresses, msg_text)
 


