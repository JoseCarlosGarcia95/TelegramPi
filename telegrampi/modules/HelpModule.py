import os
import re
from telegrampi.modules.TelegramModule import TelegramModule

class HelpModule(TelegramModule):
    
    # HELPKEY: help
    # HELP: Help menu.
    # HELP: Usage:
    # HELP:  |_ /help (<helpkey>) - Show help for a module.
    def __init__(self, Telegram):
        TelegramModule.__init__(self, Telegram)
        self.permissionlevel = 3
        self.helpdata = self.autodiscoverhelp()
        
    def autodiscoverhelp(self):
        files = os.listdir(os.path.dirname(os.path.abspath(__file__)))  #files and directories

        modules = []
        for file in files:
            if file.endswith('.py') and file != '__init__.py' and file != 'TelegramModule.py':
                modules.append(file)

        helpdict = dict()
        for module in modules:
            module_file = open(os.path.dirname(os.path.abspath(__file__)) + '/' + module, 'r')
            module_raw  = module_file.read()
            module_file.close()

            matches = re.search(r"# HELPKEY: (.*)", module_raw)
            if matches:
                helpkey = matches.group(1)
                helpdict[helpkey] = ''

                matches = re.finditer(r"# HELP: (.*)", module_raw)

                for matchNum, match in enumerate(matches):                    
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1

                        if match.group(groupNum) != '(.*)' and match.group(groupNum) != '(.*)", module_raw)':
                            helpdict[helpkey] += match.group(groupNum) + "\n"


        return helpdict
    """
    Process the telegram response.
    """
    def processCommand(self, command_body, sender_id):
        output = ""

        parameters = self.splitbody(command_body)
        helpkey    = parameters[0]

        if helpkey == '':
            for help in self.helpdata.keys():
                output += help + ":\n"
                output += self.helpdata[help]
                output += "\n\n"
        else:
            output += helpkey + ":\n"
            output += self.helpdata[helpkey]
            output += "\n\n"

        self.telegram.sendMessage(sender_id, output)
