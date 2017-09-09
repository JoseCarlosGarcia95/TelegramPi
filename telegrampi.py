#!/usr/bin/python

import configparser
from telegrampi.telegram import Telegram

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Initialize a new Telegram API
    tg = Telegram(config)
    tg.updatetask()

main()
