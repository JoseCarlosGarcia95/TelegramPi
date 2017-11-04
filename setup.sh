#!/bin/bash

# Packages needed for TelegramPi
PACKAGES=("python-configparser" "python-nmap" "nmap" "python-pyaes" "python-m2crypto")

for PACKAGE in ${PACKAGES[*]}; do
    if [ $(dpkg-query -W -f='${Status}' $PACKAGE 2>/dev/null | grep -c "ok installed") -eq 0 ];
    then
        sudo apt install $PACKAGE
    fi
done

# Configuration generator.
if [[ ! -f config.ini ]];
then
    echo -n "Please enter telegram username of super user [ENTER]: "
    read SUPER_USER
    
    echo -n "Please enter telegram token and then [ENTER]: "
    read TELEGRAM_TOKEN

    echo -n "Please enter a path for downloading files [ENTER]: "
    read DOWNLOAD_PATH

    CONFIG_INI="[Telegram-Info]\nbot-token=$TELEGRAM_TOKEN\n\nsuper-user=$SUPER_USER\n[Modules]\ndownload-file-path=$DOWNLOAD_PATH"

    echo -e "$CONFIG_INI" > config.ini
    chmod 777 config.ini
fi
