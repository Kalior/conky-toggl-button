#! /usr/bin/python

import requests
# parsing json data
import json
import sys
from tkinter import *

auth_fields = requests.auth.HTTPBasicAuth(API_TOKEN,'api_token')

def update_time_entry_project(project_id):
  try:
    url_current = 'https://www.toggl.com/api/v8/time_entries/current'

    r = requests.get(url_current, auth=auth_fields)
    data = json.loads(r.text)['data']
    if(data == None):
        return
    else:
      url_entry = "https://www.toggl.com/api/v8/time_entries/" + str(data['id'])
      payload = {'time_entry':{"pid":project_id}}
      headers = {'Content-Type': 'application/json'}
      r = requests.put(url_entry, auth=auth_fields, headers=headers, data=json.dumps(payload))
  except:
    return

def update_projects(frame):
  try:
    url_clients = 'https://www.toggl.com/api/v8/clients'
    clients_request = requests.get(url_clients, auth=auth_fields)
    all_clients = json.loads(clients_request.text)
    all_projects = []
    for client in all_clients:
      projects_url = 'https://www.toggl.com/api/v8/clients/'+ str(client['id']) +'/projects'
      projects_request = requests.get(projects_url, auth=auth_fields)
      projects = json.loads(projects_request.text)
      if (projects != None):
        for project in projects:
          project['client_name'] = client['name']
          all_projects.append(project)
    with open('/home/kalior/projects/conky-toggl-button/toggl_projects', 'w') as f:
      f.write(json.dumps(all_projects))
    frame.destroy()
    new_frame = Frame()
    new_frame.grid(row=0,column=0)
    add_projects_to_list(new_frame)
  except:
    return

def get_projects():
  with open('/home/kalior/projects/conky-toggl-button/toggl_projects', 'r') as f:
    all_projects = json.loads(f.read())
    return all_projects

def add_projects_to_list(frame):
  b = Button(frame, text = "Update projects", command = lambda f=frame: update_projects(f), font = "Inconsolata 14")
  b.pack(fill=X)
  for project in get_projects():
    b = Button(frame, text = project['client_name'] + " " + project['name'], command = lambda id=project['id']: do_and_quit(id), font = "Inconsolata 14")
    b.pack(fill=X)

def do_and_quit(project_id):
  master.destroy()
  update_time_entry_project(project_id)

def quit(event):
  master.destroy()

master = Tk()
master.title("Toggl Conky pop-up")

x = int(sys.argv[1])
y = int(sys.argv[2])

master.geometry('+%d+%d' % (x, y - len(get_projects())*25))

frame = Frame(master)
frame.grid(row=0,column=0)

add_projects_to_list(frame)

master.bind('<Escape>', quit)
mainloop( )
