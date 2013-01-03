#!/usr/bin/env python
#
# Facebook Poke Response Bot
# By Brandon Smith (brandon.smith@studiobebop.net)
#
# Requires :
#  - Python 2.7
#    http://python.org
#  - Requests
#    http://docs.python-requests.org/en/latest/index.html
#  - BeautifulSoup
#    http://www.crummy.com/software/BeautifulSoup/
#

import sys
import time
import getpass
import urllib
import urllib2
import random
import ssl
import requests
import BeautifulSoup
import form_processor

###
# Global Config
###

username = raw_input("[+] Facebook Email: ")
password = getpass.getpass("[+] Facebook Password (will not show): ")
session     = None
facebook_id = ""
sleep_time  = input("[+] Enter sleep time in seconds: ")

#!# End Config #!#

# Misc Functions

def debug_form(url, data):
    print
    print "[+] Action : %s" % url
    for key in data:
        print "\"%s\" => \"%s\"" % (key, data[key])
    print
    
def show_status(message):
    sys.stdout.write("[+] %s, " % message)
    sys.stdout.flush()

def get_random_useragent():
    base_agent = "Mozilla/%.1f (Windows; U; Windows NT 5.1; en-US; rv:%.1f.%.1f) Gecko/%d0%d Firefox/%.1f.%.1f"
    return base_agent % ((random.random() + 5),
                         (random.random() + random.randint(1, 8)), random.random(),
                         random.randint(2000, 2100), random.randint(92215, 99999),
                         (random.random() + random.randint(3, 9)), random.random())

def strip_html(string):
    new_str = ""
    in_tag = False
    for char in string:
        if char == "<":
            in_tag = True
        elif char == ">":
            in_tag = False
        else:
            if not in_tag:
                new_str += char
    return new_str.strip()

def get_phstamp(data):
    phstamp = "1"

    string = urllib.urlencode(data)
    input_len = len(string)

    for char in data["fb_dtsg"]:
        phstamp += "%d" % ord(char)
    phstamp = "%s%d" % (phstamp, input_len)

    return phstamp

# Main Functions

def login():
    global facebook_id
    show_status("Logging in")

    start_url = "http://facebook.com/"
    page = session.get(start_url).content.decode('utf-8', 'replace')
    forms = form_processor.parse_forms(start_url, page)
    form = forms[0]
    form_action = form["action"]
    referer = form_action
    form_data = form["inputs"]
    form_data['email'] = username
    form_data['pass'] = password
    request = session.post(form_action, form_data)

    print "Done"

    if "Log Out" not in request.content:
        return False

    facebook_id = request.content.split("({\"user\":\"")[1].split("\"")[0]

    return True

def check_for_pokes():
    show_status("Checking for pokes")
    page = session.get("https://www.facebook.com/pokes?notif_t=poke").content
    friend_ids = []
    data = {}

    chunks = page.split("has poked you.</div><")
    if len(chunks) > 1:
        for item in chunks:
            if not "data-hovercard=\"/ajax/hovercard/user.php?id=" in item:
                continue
            item = item.split("data-hovercard=\"/ajax/hovercard/user.php?id=")[-1]
            friend_id = item.split("\"")[0]
            friend_ids.append(friend_id)

        soup = BeautifulSoup.BeautifulSoup(page)
        filter_names = ["fb_dtsg", "__user", "__a", "__req"]
        for tag in soup.findAll("input"):
            if not tag.has_key("name"):
                continue
            name = tag["name"]
            if name not in filter_names:
                continue
            data[name] = tag['value']

    return data, friend_ids

def poke_user(data, friend_id):
    post_url = "https://www.facebook.com/ajax/pokes/poke_inline.php"

    # Set up POST data
    pdata = {}
    pdata["uid"] = friend_id
    pdata["pokeback"] = "1"
    pdata["nctr[_mod]"] = "pagelet_pokes"
    pdata["__user"] = facebook_id
    pdata["__a"] = "1"
    pdata["__req"] = "8"
    pdata["fb_dtsg"] = data["fb_dtsg"]
    pdata["phstamp"] = get_phstamp(pdata)

    # Submit poke
    request = session.post(post_url, pdata)
    content = request.content

if __name__ == '__main__':
    session = requests.session(headers={"User-Agent": get_random_useragent()})

    # Log on in
    if not login():
        print "+" * 85
        print "[!] Error!"
        print "[!] Failed to log in to Facebook with the username and password provided."
        raw_input("[+] Press enter to exit...")
        exit()

    print
    print "[!] Here we go, press Ctrl+Break to exit."

    while True:
        print
        print "-" * 85

        try:
            data, friend_ids = check_for_pokes()
            if len(friend_ids) == 0:
                print "None found!"
            else:
                print "Done"
                print "[+] Found %d pokes to return." % len(friend_ids)
                show_status("Poking back")
                for friend_id in friend_ids:
                    poke_user(data, friend_id)
                print "Done"
        except:
            print
            print "[!] Something blew up, bailing out!"

        for i in range(sleep_time, -1, -1):
            sys.stdout.write("\r[+] Sleeping for %d seconds...\t" % i)
            time.sleep(1)
        print

        print "-" * 85

    # All done
    print
    print "-" * 85
    print "[+] All done..."
    raw_input("[+] Press enter to exit...")