#!/usr/bin/env python3

import http.client

# Use the GET method

conn = http.client.HTTPConnection('www.linkedinsolutions.com')
conn.request("GET", "/")
resp1 = conn.getresponse()
print(resp1.status, resp1.reason)
data1 = resp1.read()
print(data1)