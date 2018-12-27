#!/usr/bin/python3

import urllib.parse

from mycommon import JsonFile


def get_fitbit_auth_url(auth_url, scope, client_id, redirect_uri):

    # Using OAuth 2.0 — MB Web API Docs
    # Authorization Code Grant Flow: Authorization Page
    # https://developer.mercedes-benz.com/content-page/oauth-documentation

    params = {
        "client_id": client_id,
        "response_type": "code",
        "scope": scope,
        "redirect_uri": redirect_uri,
    }

    qs = urllib.parse.urlencode(params)

    return auth_url + "?" + qs


auth_url = "https://api.secure.mercedes-benz.com/oidc10/auth/oauth/v2/authorize"
scope = "mb:vehicle:status:general mb:user:pool:reader mb:vehicle:mbdata:evstatus"
auth = JsonFile("mb-auth.json").read()

mb_auth_url = get_fitbit_auth_url(
    auth_url, scope, auth["client_id"], auth["callback_url"])
print("{}".format(mb_auth_url))
