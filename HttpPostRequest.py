#!/usr/bin/env python3

# Use the POST method:

import http.client
import urllib.parse

params = urllib.parse.urlencode({'@number': 12524, '@type': 'issue', '@action': 'Show'})
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
newconn = http.client.HTTPConnection("www.linkedinsolutions.com")
newconn.request("POST", "", params, headers)
response = newconn.getresponse()
print(response.status, response.reason)
