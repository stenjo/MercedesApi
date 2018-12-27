#!/usr/bin/python3

from urllib.error import URLError
from urllib.request import Request, urlopen
import json
import pprint

from mycommon import JsonFile, DateTime


def get_activity(auth_value):

    # Using OAuth 2.0 — Fitbit Web API Docs
    # Making Requests
    # https://dev.fitbit.com/docs/oauth2/#making-requests

    # Activity & Exercise Logs — Fitbit Web API Docs
    # https://dev.fitbit.com/docs/activity/

    # url = "https://api.mercedes-benz.com/vehicledata/v1/vehicles/{}/stateofcharge"
    url = "https://api.mercedes-benz.com/experimental/connectedvehicle/v1/vehicles/{}/stateofcharge"
    # url = url.format('WDD2428901J011537')
    url = url.format('A820F9815BC89D1CE1')
    req = Request(url)
    req.add_header("Authorization", auth_value)
    req.add_header("accept","application/json;charset=utf-8")

    try:
        res = urlopen(req)
    except URLError as e:
        print(e)
        content = e.read().decode("utf-8")
        e.close()
        return content
    else:
        content = res.read().decode("utf-8")
        res.close()
        return content

token_type = "Bearer"
jsonfile = JsonFile("mb-auth.json")
auth = jsonfile.read()

# yyyy-mm-dd
date = DateTime.yyyymmdd(DateTime.yesterday())
# date = "2016-07-30" # yyyy-MM-dd

auth_value = "{} {}".format(token_type, auth["access_token"])
# print(auth_value)

activity_json = get_activity(auth_value)
pprint.pprint(json.loads(activity_json))
