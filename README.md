Currently some experimental foolings around with Gmail to try to, for example,
download all my email.

There's "get_mail.py", which downloads mail from Gmail via IMAP. Don't ask me
about specifics, I pretty much just pasted it all together from the internet.
Saves all the emails in a directory, one email per file.

Then there's process_mail.py, which reads in all those emails and spits them out
as other emails in another directory, but with less garbage attached. Not a
strictly necessary step, but useful so that the total size of the files we're
working with is a bit smaller.

word_counts.py is there to look up the word length of emails that the 2012
HCII cohort has sent me. cohort_emails.txt and chart_etc.xslx are the output
of word_counts.py.

