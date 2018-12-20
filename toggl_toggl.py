#! /usr/bin/python

import requests

# parsing json data
import json

auth_fields = requests.auth.HTTPBasicAuth(API_TOKEN, "api_token")
headers = {"Content-Type": "application/json"}


def toggl_toggl():
    try:
        url_current = "https://www.toggl.com/api/v8/time_entries/current"
        r = requests.get(url_current, auth=auth_fields)
        data = json.loads(r.text)["data"]
        if data == None:
            start_toggl()
        else:
            stop_toggl(str(data["id"]))
    except:
        return


def start_toggl():
    url_start = "https://www.toggl.com/api/v8/time_entries/start"
    payload = {
        "time_entry": {"description": "i3-conky-time-entry", "created_with": "i3-conky"}
    }
    r = requests.post(
        url_start, auth=auth_fields, headers=headers, data=json.dumps(payload)
    )
    return r.text


def stop_toggl(entry_id):
    url_stop = "https://www.toggl.com/api/v8/time_entries/" + entry_id + "/stop"
    r = requests.put(url_stop, auth=auth_fields, headers=headers)


if __name__ == "__main__":
    toggl_toggl()
