#!/usr/bin/env python
#
# Functions that may be useful as we deal with emails a bunch.
#
import datetime

class email:
    """ represents an email """
    def __init__(self, date, from_address, to_addresses, cc_addresses, text):
        self.date = date
        self.from_address = from_address
        self.to_addresses = to_addresses
        self.cc_addresses = cc_addresses
        self.text = text


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
    date_string = contents[0].strip()
    #TODO: I never specified that the string should be in this format when
    # it is written to the file in the first place. I should do that.
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    from_address = contents[1].strip()
    # note that we expect to_addresses to be safe
    to_addresses = eval(contents[2].strip())
    cc_addresses = eval(contents[3].strip())
    msg_lines = contents[4:]
    msg_lines_noreplies = remove_replies(msg_lines)
    msg_text = ''.join(msg_lines_noreplies)

    return email(date, from_address, to_addresses, cc_addresses, msg_text)
 


