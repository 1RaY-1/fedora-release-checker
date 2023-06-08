# What is it
A Python that checks if there is a new Fedora Workstation release and notifies user about new release by sending an email 

# Setup
* Enable less secure apps to access Gmail
* Turn on 2-Step Verification
* Create app password
* Install needed pip modules, by typing ```pip install -r requirements.txt``` or ```pip install requests bs4```
* On line 108 in the program, before executing it: enter currently the latest fedora release, your gmail account, your gmail password for apps, check delay (in seconds)
* execute it by typing ```python check_fedora_release.py```

It will check the official download website for new release every X seconds (depends on what you enter as 'check_delay') and if there is a new release, it sends you a gmail and program stops.

I suggest running this as a background process.

This program could be used to check any other stuff from websites.
