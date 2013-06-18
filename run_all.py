#!/usr/bin/env python

# One script to run them all! You should be able to set this up, enter user
# name and password, and forget about it!

from subprocess import call

print "This application will attempt to save all your gmail to files.\
 If this is not what you want, quit now with ctrl-c." 
print "Make sure your computer is set to not sleep. (on a mac, set this in\
 System Preferences -> Energy Saver)"
print "Also, make sure there's no folder called emails/ already; if there is,\
 it'll get clobbered."
email_address = raw_input("Enter your email address: ")
retval = call(['./get_mail.py', '--email_address=' + email_address])
if retval == 0:
    retval = call(['./process_mail.py'])
