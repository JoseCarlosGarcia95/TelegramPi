import urllib2, urllib, json, threading

# Modules
from telegrampi.modules.DownloadFile import DownloadFile

class Telegram:

    """
    Retrieve telegram api URL.
    """
    def __init__(self, config):
        self.config = config
        self.apiurl = "https://api.telegram.org/bot{}/".format(config['Telegram-Info']['bot-token'])

        self.initializehandlers()

    """
    Make a request to telegram bot api.
    """
    def request(self, path, parameters=[]):
        url = self.apiurl + path + '?' + urllib.urlencode(parameters)

        response = urllib2.urlopen(url)
        html = response.read()

        response.close()

        return html

    """
    Initialize handlers.
    """
    def initializehandlers(self):
        self.handlers = dict()

        self.handlers['download'] = DownloadFile(self)

    """
    Make a request and return JSON as response.
    """
    def requestjson(self, path, parameters=[]):
        return json.loads(self.request(path, parameters))

    """
    Update the offset for the next request.
    """
    def updateoffset(self, offset):
        self.config.set('Telegram-Info', 'updates-offset', str(offset))

        with open('config.ini', 'wb') as configfile:
            self.config.write(configfile)

    """
    Main telegram process thread.
    """
    def _updatethread(self):
        # Get updates.
        updates_json = self.requestjson('getUpdates', {'offset' : self.offset})

        if updates_json['ok']:
            for item in updates_json['result']:
                message = item['message']
                message_text = message['text']

                sender = message['from']
                sender_id       = sender['id']

                commands_tmp    = message_text.split(' ')
                command         = commands_tmp[0]

                command_body    = ''

                if len(commands_tmp) > 1:
                    command_body    = message_text[len(command)+1:]

                if command in self.handlers.keys():
                    try:
                        self.handlers[command].processCommand(command_body, sender_id)
                    except Exception as err:
                        self.sendMessage(sender_id, "error on command {}, {}".format(command, err))
                else:
                    self.sendMessage(sender_id, command + " command not found")

                # Update offset
                self.offset = item['update_id'] + 1
                self.updateoffset(self.offset)

        threading.Timer(2.0, self._updatethread).start()


    """
    Initialize telegram function.
    """
    def updatetask(self):
        if self.config.has_option('Telegram-Info', 'updates-offset'):
            self.offset = int(self.config['Telegram-Info']['updates-offset'])
        else:
            self.updateoffset(0)
            self.offset = 0

        self._updatethread()

    """
    Send a message to user_id.
    """
    def sendMessage(self, user_id, message):
        self.request('sendMessage', {'chat_id' : user_id, 'text': message})
