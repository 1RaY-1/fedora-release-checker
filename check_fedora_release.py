#!/usr/bin/env python3

"""
Program that checks for new Fedora Workstation release
And notifies user about new release by sending an email
"""

import requests
from bs4 import BeautifulSoup as BS 
from time import sleep
import sys
import smtplib

class FedoraChecker:

    def __init__(self, v, target_gmail, gmail_passwd, delay):
        self.v = v

        # needed page
        self.url = "https://getfedora.org/en/workstation/download/"

        # delay of checking in seconds
        self.delay  = delay

        # set to False if will run this program in background, set to True if want to see logs
        self.print_logs = False

        # remove this from fedora release, to make clear release version
        self.chars_to_remove = ["Fedora", "Download", "Workstation", ".", " "]

        # for gmail
        self.target_gmail = target_gmail
        self.gmail_passwd = gmail_passwd
        self.subject = "Fedora Workstation"
        self.body = f"""
There is a new Fedora Workstation release!
You can check it here: {self.url}


PS: Now you'll have to change it in {sys.argv[0]}"""
        self.message = f"Subject: {self.subject}\n\n{self.body}"

    # will save time
    def ifprint_logs(self, status ,msg):
        if self.print_logs:
            if status == "info":
                print("\033[01;33m[INFO]\033[00m " + str(msg))
            elif status == "error":
                print(f"\033[01;31m[ERROR]\033[00m " + str(msg))
            else:
                raise TypeError ("In function 'ifprint_logs' status can only be 'info' or 'error'")

    def notify(self):
        try:
            self.ifprint_logs("info", f"Notifying {self.target_gmail} about new Fedora release...")

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login(self.target_gmail, self.gmail_passwd)

            server.sendmail("admin@fedora_notifier.com", self.target_gmail, self.message)
            server.quit()
            sys.exit()

        except smtplib.SMTPConnectionError:
            self.ifprint_logs("error", "SMTP connection failed")
        except:
            self.ifprint_logs("error", "An error occurred")
        finally:
           # exit
            self.ifprint_logs("info", "Exiting...")
            sys.exit()

    def check(self):
        self.ifprint_logs("info", "Checking...\n")

        r = requests.get(self.url)
        soup = BS(r.text, 'html.parser')
        
        # here's stored the latest release
        new_v = soup.find_all('h1')[0].get_text() 

        for c in self.chars_to_remove:
            new_v = new_v.replace(c, "")

        if self.v != new_v:
            self.ifprint_logs("info", f"There is a new Fedora release: {new_v}")
            self.notify()
        else:
            pass

    def main(self): 
        
        try:
            while True:
                self.check()
                sleep(self.delay)
        except Exception as e:
            self.ifprint_logs("error", "\nAn exception occured:\n" )
            sys.exit()
        

if __name__ == '__main__':
    # latest fedora release for the moment (for the moment it's 34), your gmail account, your gmail password for apps, check delay
    fn = FedoraChecker("34", "YOUR_GMAIL", "YOUR_GMAIL_PASSWORD_FOR_APPS", check_delay)

    fn.main()

