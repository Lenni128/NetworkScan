#!/bin/bash

show_help() {
  echo "Usage: $(basename "$0") [OPTION]"
  echo "  -i <IP>     set IP-Adress"
  echo "  -U <User>   set username from SSH-Server"
  echo "  -h          show this help text"


}

while getopts ":i:U:" opt; do
  case $opt in
    i)
      ip_address="$OPTARG"
      ;;
    U)
      user_name="$OPTARG"
      ;;
    \?)
      echo "Ungültige Option: -$OPTARG"
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
  esac
done

if [ -z "$ip_address" ] || [ -z "$user_name" ]; then
  echo "Error: You need to specify both an IP address and a username."
  echo ""
  show_help
  exit 1
fi



echo "Installing MQTT..."
echo ""
echo "Username:" $user_name
homedirectory="/home/"$user_name

# Kopieren des Software-Ordners auf den Server
scp -r software/ $user_name@$ip_address:$homedirectory
echo ""

cd software
chmod +x start.sh

# Ausführen von Befehlen auf dem Server
ssh $user_name@$ip_address "
    cd software &&
    sudo apt update -y &&
    sudo apt upgrade -y &&
    sudo apt install python3-pip -y &&
    pip3 install python-nmap &&
    pip3 install python3-nmap &&
    sudo apt-get install nmap
    pip3 install python3-smtplib
"

echo "Done!"