import datetime
import json
import os

import jwt
import requests
from django.conf import settings
from requests.exceptions import HTTPError


def delete_scene_objects(scene, token: jwt):
    # delete scene from persist
    host = os.getenv("HOSTNAME")
    # in docker on localhost this url will fail
    url = f"https://{host}/persist/{scene}"
    result = _urlopen(url, token, "DELETE")
    return result


def get_persist_scenes(token: jwt, user):
    # request all _scenes from persist
    host = os.getenv("HOSTNAME")
    # in docker on localhost this url will fail
    if user.is_authenticated:
        if user.is_staff:
            url = f"https://{host}/persist/!allscenes"
        else:
            url = f"https://{host}/persist/{user.username}/!allscenes"
        result = _urlopen(url, token, "GET")
        if result:
            return json.loads(result)
    return []


def _urlopen(url, token: jwt, method):
    if not token:
        print("Error: mqtt_token for persist not available")
        return None
    headers = {"Cookie": f"mqtt_token={token.decode('utf-8')}"}
    cookies = {"mqtt_token": token.decode("utf-8")}
    verify = not settings.DEBUG
    print(headers)
    print(cookies)
    print(verify)
    print(url)
    print(method)
    try:
        if method == "GET":
            response = requests.get(
                url,
                #headers=headers,
                cookies=cookies,
                verify=verify
            )
        elif method == "DELETE":
            response = requests.delete(
                url, headers=headers, cookies=cookies, verify=verify
            )
        return response.text
    except (requests.exceptions.ConnectionError, HTTPError) as err:
        print("{0}: ".format(err) + url)
    return None
