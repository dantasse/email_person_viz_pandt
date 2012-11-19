Code for a class project that aims to download all of our email and pull out
some hopefully-meaningful statements.

### Important files: 

get\_mail.py: downloads mail from Gmail via IMAP. Don't ask me
about specifics, I pretty much just pasted it all together from the internet.
Saves all the emails in a directory, one email per file.

process\_mail.py: reads in all those emails and spits them out
as other emails in another directory, but with less garbage attached. Not a
strictly necessary step, but useful so that the total size of the files we're
working with is a bit smaller.

generate\_snippets.py: the script that actually picks out relevant snippets
from your email.

email\_lib.py: some functions that are called from other scripts.

### Not important:

\_\_init\_\_.py is just a marker that tells python it's okay to look in this
directory for other python files in "import" statements; don't worry about it.

word\_counts.py is there to look up the word length of emails that the 2012
HCII cohort has sent me. cohort\_emails.txt and chart\_etc.xslx are the output
of word\_counts.py.

