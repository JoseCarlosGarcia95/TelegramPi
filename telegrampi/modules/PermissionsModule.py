from telegrampi.modules.TelegramModule import TelegramModule

class PermissionsModule(TelegramModule):
    # HELPKEY: permissions
    # HELP: Permission manager.
    # HELP: Usage:
    # HELP:  |_ /permissions - List users and permissions.
    # HELP:  |_ /permissions update <username> <level> - Update <user> with <level>
    def __init__(self, Telegram):
        TelegramModule.__init__(self, Telegram)
        self.permissionlevel = 10
        
    """
    Process the telegram response.
    """
    def processCommand(self, command_body, sender_id):
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

    
    def listusers(self, arguments, sender_id):
        output   = "| Users\n"

        users = self.telegram.permissions.listusers()

        for user in users.keys():
            output += "| " + user + " => " + users[user] + "\n"

        self.telegram.sendMessage(sender_id, output)

    def update(self, arguments, sender_id):
        if len(arguments) < 3:
            self.telegram.sendMessage(sender_id, '3 arguments needed')
        else:
            username = arguments[1]
            level    = arguments[2]

            self.telegram.permissions.updatepermissions(username, level)

            self.listusers(arguments, sender_id)
