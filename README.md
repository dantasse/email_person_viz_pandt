Code for a class project that aims to download all of our email and pull out
some hopefully-meaningful statements.

## Instructions:
1. Make sure you have python. Open a terminal and run:

        python --version
If it comes back with 2.7 or higher, you're in good shape. (if it's lower, stuff might still work, but this was written in 2.7.)
2. Install NLTK (Natural Language Toolkit): Go to <http://pypi.python.org/pypi/nltk/2.0.4>, download the zip, unzip it to a folder. Navigate to that folder in a terminal, and run:

        sudo python setup.py install
<!--3. Get the Punkt tokenizer; this is the bit that can split text into sentences neatly. To do so, at a terminal:

        python
        import nltk
        nltk.download()
Now you'll see a window pop up; navigate to "Models" then select Punkt and download.-->
4. Get all of the code for this project. Two options: First, you can run:

        git clone https://github.com/dantasse/email_person_viz_pandt.git
And then whenever you want to update the code (e.g. when we add more rules) you can just go to that same directory and then run:
 
        git pull
And you'll be up to date. On the other hand, if you don't want to, or if you don't have git installed and don't want to install it, you can just do Option 2: download <https://github.com/dantasse/email_person_viz_pandt/archive/master.zip> and unzip it.
5. Navigate to the folder where you downloaded/cloned it, in a terminal.
6. Run:

        ./get_mail.py (path)
where (path) is an existing directory where you want to save all your emails. For example:

        ./get_mail.py /Users/dtasse/Desktop/emails/
(be sure to create that directory first.) This script will ask you for your gmail username and password, then it'll just download them all. If you use 2-factor, you'll need an app-specific password for this; if this sentence makes no sense to you then just ignore it (and ask Dan about why 2-factor is cool and you should probably do it, but that's unrelated to this project). It'll take a while (probably about 20 minutes per 10,000 messages).
7. Run:

        ./process_mail.py (raw_email_path) (output_path)
where (raw\_email\_path) is the directory you just downloaded your emails into in the previous step, and (output\_path) is the directory you want to save the processed emails to. Make sure these directories both already exist. Example:

        ./process_mail.py /Users/dtasse/Desktop/emails/ /Users/dtasse/Desktop/processed_emails/
(this will be quicker. Seconds or minutes.)
8. Now the fun part! Run generate\_snippets.py. There are a lot of options to generate\_snippets.py, so just run generate\_snippets.py -h to see all the things you can do. Some examples:

        ./generate_snippets.py me@me.com you@you.com -p (path to processed emails)
will just find snippets in all the emails between me@me.com and you@you.com.

        ./generate_snippets.py me@me.com you@you.com --start-date=2012-08-01 --end-date=2012-08-31 -p (path to processed emails)
will find snippets in all the emails between these two addresses in August 2012.
Currently (as of 11/18/12) this has a very simple algorithm for picking out "meaningful" sentences: just looks for sentences with any of the following words: [':)', ':-)', 'lol', 'love', 'i feel', 'xoxo']. If you want to fiddle around with different ways to find meaningful sentences, generate\_snippets is the place to start. 

## More Details:

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

### Credits:
english.pickle is the English sentence segmenter from Punkt, included in NLTK,
which is amazing. More info: <http://nltk.org/>

