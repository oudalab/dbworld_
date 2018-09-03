#! /usr/bin/python3
"""
Read the updates from https://research.cs.wisc.edu/dbworld/browse.html
and turn each row into json objects.

Example:
    {
        "date": "02-Sep-2018",
        "msgtype": "conf. ann.",
        "from": "Jesson Butt",
        "subject": "Call for poster and demo: IEEE ISPA2018 (Parallel and Distributed Processing with Applications)",
        "subjecturl": "http://www.cs.wisc.edu/dbworld/messages/2018-09/1535939350.html",
        "deadline": "1-Oct-2018",
        "webpage": "http://www.swinflow.org/confs/2018/ispa/"
    }

Posts the subject text.
The message turns the msg type into a hash tag

# Thanks https://medium.com/mai-piu-senza/connect-a-python-script-to-ifttt-8ee0240bb3aa
"""


import datetime
import json
import logging
import pdb
import shelve

import requests
from bs4 import BeautifulSoup


url = "https://research.cs.wisc.edu/dbworld/browse.html"
dbworldfile = "dbworld.shelve"


def check():
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "lxml")

    # Collect rows until we are on a different date or we've already sent
    # something
    data = []
    with shelve.open("dbworld.shelve") as s:
        if "rows" in s:
            rows = s["rows"]
        else:
            rows = []

        for row in soup.find_all('tbody'):
            row = {i:col for i,col in enumerate(row.find_all('td'))}
            webpage = "" if row[5].find("a") is None else row[5].find("a")["href"]
            subjecturl = "" if row[3].find("a") is None else row[3].find("a")["href"]
            msg = {
                "date": row[0].text.strip(),
                "msgtype": row[1].text.strip(),
                "from": row[2].text.strip(),
                "subject": row[3].text.strip(),
                "subjecturl": subjecturl.strip(),
                "deadline": row[4].text.strip(),
                "webpage": webpage.strip()
            }
            if msg in rows:
                break
            rows.append(msg)
            print(json.dumps(msg))
            notification(msg) # Send the notification

        # Save all the new rows
        s["rows"] = rows


msgtypemap = {
        "conf. ann." : "#conference",
        "job ann.": "#jobalert",
        "journal CFP": "#journal",
        "journal ann.": "#journal",
        "news": "#news",
        "grant": "#grant",
        "book ann.": "#book",
        }


def notification(message):
    """Post the message to ifttt:
        `value1` is the message text.
    """
    subject = message["subject"]
    subjecturl = message["subjecturl"]
    thehash = msgtypemap.get(message["msgtype"], message["msgtype"])
    webpage = message["webpage"]
    message = f"{subjecturl} {subject} {thehash} {webpage}"
    report = {"value1": message}
    req = requests.post("https://maker.ifttt.com/trigger/dbworld_post/with/key/cqhdzjBquODIvTezwtIiv1", data=report)
    print(req.text)


def main():
    check()


if __name__ == '__main__':
    main()
    pass

