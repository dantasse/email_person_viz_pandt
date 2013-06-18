Code to download and somewhat parse your gmail archives.

## Instructions:
1. Make sure you have python. Open a terminal and run:

        python --version
If it comes back with 2.7 or higher, you're in good shape. (if it's lower, stuff might still work, but this was written in 2.7.)

4. Get all of the code for this project. Two options: First, you can clone this repo (see details around github help), or if you don't have git installed and don't want to install it, you can just do Option 2: go to the github page and unzip it.
5. Navigate to the folder where you downloaded/cloned it, in a terminal.
6. Run:

        ./run_all.py
This script will ask you for your gmail username and password, then it'll just download them all, into a new folder it will created called emails/. If you use 2-factor, you'll need an app-specific password for this; if this sentence makes no sense to you then just ignore it (and ask Dan about why 2-factor is cool and you should probably do it, but that's unrelated to this project). It'll take a while (for Dan's 60k messages, 2.3 gb, it took about 20 minutes).

### Important files: 

get\_mail.py: downloads mail from Gmail via IMAP. Don't ask me
about specifics, I pretty much just pasted it all together from the internet.
Saves all the emails in a directory, one email per file.

process\_mail.py: reads in all those emails and spits them out
as other emails in another directory, but with less garbage attached. Not a
strictly necessary step, but useful so that the total size of the files we're
working with is a bit smaller.

email\_lib.py: some functions that are called from other scripts.

