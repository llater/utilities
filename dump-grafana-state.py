#!/usr/bin/env python

import json, os, requests

GRAFANA_API_TOKEN = os.environ["GRAFANA_API_TOKEN"]
GRAFANA_API_URL = os.environ["GRAFANA_API_URL"]

all_dashboards_endpoint = "/search?folderIds=0&query"
dashboard_by_uid_endpoint = "/dashboards/uid/"

# Determine the uid of each dashboard
headers = {"Authorization": "Bearer %s" % GRAFANA_API_TOKEN}
url = GRAFANA_API_BASE_URL + all_dashboards_endpoint
response = requests.get(url, headers=headers)
if response.status_code != requests.codes.ok:
  print response.text.encode('utf-8')
  raise Exception("Call to url \"%s\" failed with status: %s" % (url, response.status_code))

dashboard_uids = []
for dashboard in response.json():
  dashboard_uids.append(dashboard["uid"])

# For each dashboard, write its contents as pretty-printed JSON
for uid in dashboard_uids:
  url = GRAFANA_API_BASE_URL + dashboard_by_uid_endpoint + uid
  response = requests.get(url, headers=headers)
  if response.status_code != requests.codes.ok:
    print response.text.encode('utf-8')
    raise Exception("Call to url \"%s\" failed with status: %s" % (url, response.status_code))

  name = response.json()["meta"]["slug"] + ".json"
  with open(name, "w") as file:
    file.write(json.dumps(response.json(), indent=4))
