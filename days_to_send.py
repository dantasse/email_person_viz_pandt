#!/usr/bin/env python

# Given a first day, generate all the days to send a postcard.
from datetime import date, timedelta
import random

print "Enter the month (number) of the first interview date"
month = int(raw_input())
print "Enter the day (number) of the first interview date"
day = int(raw_input())
first_interview = date(2013, month, day)
second_interview = date(2013, month + 1, day)
third_interview = date(2013, month + 3, day)

card_days = []
current_day = first_interview
while True:
    current_day += timedelta(days=random.randint(7, 10))
    if current_day < third_interview:
        card_days.append(current_day)
    else:
        break

print "Days to send a card:"
for day in card_days:
    print day

print "Approximate interview days:"
print "First interview: " + str(first_interview)
print "Second interview: " + str(second_interview)
print "Third interview: " + str(third_interview)
