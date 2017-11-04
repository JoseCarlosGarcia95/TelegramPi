import json
import os

class Permissions:

    def __init__(self, config):
        self.config = config
        self.configpath    = os.path.dirname(os.path.abspath(__file__)) + '/../local_files/permissions.json'
        self.permissions   = self.getpermissionsfromjson()

    def getpermissionsfromjson(self):
        if not os.path.exists(self.configpath):
            return {}

        permissions_file = open(self.configpath, 'r')
        permissions      = json.loads(permissions_file.read())
        permissions_file.close()

        return permissions
        
    def permissionLevel(self, user):
        username = user['username']

        if username == self.config['Telegram-Info']['super-user']:
            return 10

        if username in self.permissions.keys():
            return self.permissions[username]
        
        return 0

    def updatepermissions(self, username, permissionLevel):
        self.permissions[username] = permissionLevel

        permissions_file           = open(self.configpath, 'w')
        permissions_file.write(json.dumps(self.permissions))
        permissions_file.close()

    def listusers(self):
        return self.permissions
