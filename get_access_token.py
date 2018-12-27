#!/usr/bin/python3

import base64
import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from mycommon import JsonFile


def get_auth_value(client_id, client_secret):

    a = "{}:{}".format(client_id, client_secret)
    b = base64.b64encode(a.encode("utf-8"))
    return "Basic {}".format(b.decode("ascii"))


def get_access_token_json(token_url, code, auth_value, redirect_uri):

    # Using OAuth 2.0 — Fitbit Web API Docs
    # Authorization Code Grant Flow: Access Token Request
    # https://developer.mercedes-benz.com/content-page/oauth-documentation#_4_request_to_exchange_the_authorization_code_with_an_access_token

    params = {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
    }

    body = urlencode(params).encode("utf-8")

    req = Request(token_url)
    req.add_header("Authorization", auth_value)
    req.add_header("Content-type","application/x-www-form-urlencoded")

    try:
        # HTTP POST
        res = urlopen(req, body)
    except URLError as e:
        print(e)
        content = e.read().decode("utf-8")
        e.close()
        return content
    else:
        content = res.read().decode("utf-8")
        res.close()
        return content


token_url = "https://api.secure.mercedes-benz.com/oidc10/auth/oauth/v2/token"

jsonfile = JsonFile("mb-auth.json")
auth = jsonfile.read()

auth_value = get_auth_value(auth["client_id"], auth["client_secret"])
print("Auht val:",auth_value)

access_token_json = get_access_token_json(
    token_url, auth["code"], auth_value, auth["callback_url"])
print("Acess token:", access_token_json)

data = json.loads(access_token_json)
auth["access_token"] = data["access_token"]
auth["refresh_token"] = data["refresh_token"]
jsonfile.write(auth)
