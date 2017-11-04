import os
import json
import pyaes
import hashlib
from telegrampi.modules.TelegramModule import TelegramModule

class PasswordModule(TelegramModule):

    def __init__(self, Telegram):
        TelegramModule.__init__(self, Telegram)
        self.permissionlevel = 7
        self.encryption_key  = None
        self.configpath = os.path.dirname(os.path.abspath(__file__)) + '/../../local_files/passwords.json'

        
    """
    Process the telegram response.
    """
    def processCommand(self, command_body, sender_id):
        arguments = self.splitbody(command_body)

        if self.encryption_key == None:
            self.setupencryption(arguments, sender_id)    
        else:            
            action    = arguments[0]
            actions   = dict()
            
            actions['list'] = self.list
            actions['show'] = self.show
            actions['update'] = self.updatedb

            if action in actions.keys():
                actions[action](arguments, sender_id)
            else:
                actions['list'](arguments, sender_id)

    def updatedb(self, arguments, sender_id):
        if len(arguments) != 4:
            self.telegram.sendMessage(sender_id, 'Please enter: /password update domain user password')
        else:
            domain   = str(arguments[1])
            user     = str(arguments[2])
            password = str(arguments[3])

            current_list = self.read(self.encryption_key)

            if not domain in current_list['data'].keys():
                current_list['data'][domain] = dict()
            current_list['data'][domain][user] = 'asd'

            self.update(self.encryption_key, current_list)
            self.telegram.sendMessage(sender_id, 'Passwords correctly updated!')

    def show(self, arguments, sender_id):
        passwords = self.read(self.encryption_key)
        output    = "@ Passwords - REMOVE THIS MESSAGE !!!\n"

        if len(arguments) > 1:
            action = str(arguments[1])
        else:
            action = 'all'

        if action == 'all':
            for domain in passwords['data'].keys():
                for user in passwords['data'][domain].keys():
                    output += "| " + domain + " | " + user + " | " + passwords['data'][domain][user] + "\n"
        elif action == 'domain':
            if len(arguments) != 3:
                self.telegram.sendMessage(sender_id, 'Please enter: /password list domain <domain>')
                return
            else:
                domain = str(arguments[2])

                if not domain in passwords['data']:
                    self.telegram.sendMessage(sender_id, 'Please enter a valid domain')
                    return

                for user in passwords['data'][domain].keys():
                    output += "| " + domain + " | " + user + " | " + passwords['data'][domain][user] + "\n"

        elif action == 'user':
            if len(arguments) != 3:
                self.telegram.sendMessage(sender_id, 'Please enter: /password list user <user>')
                return
            else:
                searchuser = str(arguments[2])
                for domain in passwords['data'].keys():
                    for user in passwords['data'][domain].keys():
                        if user == searchuser:
                            output += "| " + domain + " | " + user + " | " + passwords['data'][domain][user] + "\n"
                            
        self.telegram.sendMessage(sender_id, output)
        
    def list(self, arguments, sender_id):
        passwords = self.read(self.encryption_key)
        output    = "@ Passwords\n"

        if len(arguments) > 1:
            action = arguments[1]
        else:
            action = 'all'

        if action == 'all':
            for domain in passwords['data'].keys():
                for user in passwords['data'][domain].keys():
                    output += "| " + domain + " | " + user + " | ********\n"
        elif action == 'domain':
            if len(arguments) != 3:
                self.telegram.sendMessage(sender_id, 'Please enter: /password list domain <domain>')
                return
            else:
                domain = str(arguments[2])

                if not domain in passwords['data']:
                    self.telegram.sendMessage(sender_id, 'Please enter a valid domain')
                    return
                
                for user in passwords['data'][domain].keys():
                    output += "| " + domain + " | " + user + " | ********\n"

        elif action == 'user':
            if len(arguments) != 3:
                self.telegram.sendMessage(sender_id, 'Please enter: /password list user <user>')
                return
            else:
                searchuser = str(arguments[2])
                for domain in passwords['data'].keys():
                    for user in passwords['data'][domain].keys():
                        if user == searchuser:
                            output += "| " + domain + " | " + user + " | ********\n"
                            
        self.telegram.sendMessage(sender_id, output)

    def update(self, password, data):
        aesencrypt = pyaes.AESModeOfOperationCTR(password)
        ciphertext = aesencrypt.encrypt(json.dumps(data))

        password_file = open(self.configpath, 'w')
        password_file.write(ciphertext)
        password_file.close()

    def read(self, password):
        aesdecrypt    = pyaes.AESModeOfOperationCTR(password)
        
        password_file = open(self.configpath, 'r')
        deciphertext  = aesdecrypt.decrypt(password_file.read())
        password_file.close()

        return json.loads(deciphertext)
    
    def setupencryption(self, arguments, sender_id):
        password = arguments[0]
                   
        if len(arguments) != 1 or password == '':
            self.telegram.sendMessage(sender_id, "Please enter /password encryption_key")
        else:
            m  = hashlib.md5()
            m.update(password)
            password = m.hexdigest()

            # First setup.
            if not os.path.exists(self.configpath):
                self.update(password, {'data' : {}})

            # Check if the password is correct.
            try:
                password_data       = self.read(password)
                self.encryption_key = password
                self.telegram.sendMessage(sender_id, 'Password service is working correctly')
            except Exception as err:
                self.telegram.sendMessage(sender_id, 'You have entered an invalid password')
            
