#!/usr/bin/env python

# One script to run them all! You should be able to set this up, enter user
# name and password, and forget about it!

from subprocess import call

print "This application will attempt to save all your gmail to files.\
 If this is not what you want, quit now with ctrl-c." 
email_address = raw_input("Enter your email address: ")
retval = call(['./get_mail.py', '--email_address=' + email_address])
if retval == 0:
    retval = call(['./process_mail.py'])
if retval == 0:
    call(['./top_emailers.py', email_address])
