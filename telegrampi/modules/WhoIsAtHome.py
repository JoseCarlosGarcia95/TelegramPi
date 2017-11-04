import nmap
import os
import json
from telegrampi.modules.TelegramModule import TelegramModule

class WhoIsAtHome(TelegramModule):

    def __init__(self, Telegram):
        TelegramModule.__init__(self, Telegram)
        self.permissionlevel = 7

    # HELPKEY: whoisathome
    # HELP: Show who is at home right now.
    # HELP: Usage:
    # HELP:  |_ /whoisathome - List connected devices to router
    """
    Process the telegram response.
    """
    def processCommand(self, command_body, sender_id):
        # Read from local JSON.
        self.configpath = os.path.dirname(os.path.abspath(__file__)) + '/../../local_files/accounts-whoisathome.json'
        self.accounts   = self.getaccountsfromjson()

        # Command actions
        arguments = self.splitbody(command_body)

        action    = arguments[0]

        actions   = dict()

        actions['list'] = self.listusers
        actions['update'] = self.update

        if action in actions.keys():
            actions[action](arguments, sender_id)
        else:
            actions['list'](arguments, sender_id)

    def getaccountsfromjson(self):
        if not os.path.exists(self.configpath):
            return {}
        
        accounts_file = open(self.configpath, 'r')

        accounts      = json.loads(accounts_file.read())

        accounts_file.close()
        return accounts

    def definemacaddr(self, macaddr):
        if macaddr in self.accounts.keys():
            return self.accounts[macaddr].encode('utf-8')
        return 'Unknown'

    def listusers(self, arguments, sender_id):
        nma = nmap.PortScanner()
        mac_list = []

        results  = nma.scan(hosts='192.168.1.1-30', arguments='-sP --')

        for ip_addr in results['scan']:
            if 'mac' in results['scan'][ip_addr]['addresses'].keys():
                if results['scan'][ip_addr]['addresses']['mac'] not in mac_list:
                    mac_list.append(results['scan'][ip_addr]['addresses']['mac'])

        output   = "@ Home devices\n"

        for mac_addr in mac_list:
            output = output + "- @" + mac_addr + " | " + self.definemacaddr(mac_addr) + "\n"

        self.telegram.sendMessage(sender_id, output)

    # HELP:  |_ /whoisathome update <mac> <user> - Update a Mac Address and add it as known device.
    def update(self, arguments, sender_id):
        if len(arguments) < 3:
            self.telegram.sendMessage(sender_id, '3 arguments needed')
        else:
            macaddr = arguments[1]
            name = ''

            for i in range(2, len(arguments)):
                name = name + ' ' + arguments[i]

            self.accounts[macaddr] = name

            accounts_file = open(self.configpath, 'w')
            accounts_file.write(json.dumps(self.accounts))
            accounts_file.close()

            self.telegram.sendMessage(sender_id, 'Updated sucesfully')
