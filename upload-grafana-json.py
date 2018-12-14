#!/usr/bin/env python

import json, os, requests

GRAFANA_API_TOKEN = os.environ["GRAFANA_API_TOKEN"]
GRAFANA_API_URL = os.environ["GRAFANA_API_URL"]

create_dashboards_endpoint = "/dashboards/db" 

# For each JSON file in this directory, create a dashboard
headers = {"Authorization": "Bearer %s" % GRAFANA_API_TOKEN, "Content-Type": "application/json"}
url = GRAFANA_API_URL + create_dashboards_endpoint
files = [f for f in os.listdir(".") if (os.path.isfile(f) and f.endswith(".json"))]
for f in files:
  with open(f, "r") as db:
    content = db.read()
    # Replace dashboard.id with "null"
    db_json = json.loads(content)
    db_json["dashboard"]["id"] = "null"
    response = requests.post(url, headers=headers, data=json.dumps(db_json))
    if response.status_code != requests.codes.ok:
      print content
      print f
      print response.text.encode('utf-8')
      raise Exception("Upload call to url \"%s\" failed with status: %s" % (url, response.status_code))
