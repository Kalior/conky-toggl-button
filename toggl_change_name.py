#! /usr/bin/python

import requests

# parsing json data
import json
import sys
from tkinter import *


def update_time_entry_name(name):
    try:
        url_current = "https://www.toggl.com/api/v8/time_entries/current"
        auth_fields = requests.auth.HTTPBasicAuth(
            API_TOKEN", "api_token"
        )

        r = requests.get(url_current, auth=auth_fields)
        data = json.loads(r.text)["data"]
        if data == None:
            return
        else:
            url_entry = "https://www.toggl.com/api/v8/time_entries/" + str(data["id"])
            payload = {"time_entry": {"description": name}}
            headers = {"Content-Type": "application/json"}
            r = requests.put(
                url_entry, auth=auth_fields, headers=headers, data=json.dumps(payload)
            )
    except:
        return


def onClick(event):
    name = e.get()
    master.destroy()
    update_time_entry_name(name)


def quit(event):
    master.destroy()


master = Tk()
master.title("Toggl Conky pop-up")

w = 400
h = 20

x = int(sys.argv[1])
y = int(sys.argv[2])

master.geometry("%dx%d+%d+%d" % (w, h, x, y))


e = Entry(master, font="Inconsolata 18")
e.pack(ipady=15)

master.bind("<Return>", onClick)
master.bind("<Escape>", quit)
mainloop()
