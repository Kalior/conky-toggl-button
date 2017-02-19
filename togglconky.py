#! /usr/bin/python
import requests
# parsing json data
import json
import time
import datetime

def toggl_running():
  values = {'entry': "-", 'project_name': ""}
  try:
    auth_fields = requests.auth.HTTPBasicAuth(API_TOKEN,'api_token')

    url_entry = 'https://www.toggl.com/api/v8/time_entries/current'

    entry_request = requests.get(url_entry, auth=auth_fields)
    data = json.loads(entry_request.text)['data']

    if(data == None):
      values['entry'] = "-"
    else:
      epoch_time = int(time.time())
      duration = epoch_time + data['duration']
      entry_time = datetime.timedelta(seconds=duration)
      # stripping the seconds isn't really robust here
      values['entry'] = str(entry_time)[:4] + " " + data['description']
      values['project_name'] = "-"
      if(data['pid']):
        url_project = 'https://www.toggl.com/api/v8/projects/' + str(data['pid'])
        project_request = requests.get(url_project, auth=auth_fields)
        project_data = json.loads(project_request.text)['data']
        if(data != None):
          project_name = project_data['name']
          values['project_name'] = project_name
    return values
  except:
    return values

if __name__ == "__main__":

  entry_data = toggl_running()
  #print(entry_data)
  with open('/home/kalior/projects/conky-toggl-button/toggl_running', 'w') as f:
      f.write(entry_data['entry'])
  with open('/home/kalior/projects/conky-toggl-button/toggl_project', 'w') as f:
      f.write(entry_data['project_name'])
