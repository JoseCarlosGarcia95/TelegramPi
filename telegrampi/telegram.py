import urllib2, urllib, json, threading

class Telegram:

    def __init__(self, config):
        self.config = config
        self.apiurl = "https://api.telegram.org/bot{}/".format(config['Telegram-Info']['bot-token'])

    def request(self, path, parameters=[]):
        url = '{}{}?{}'.format(self.apiurl, path, urllib.urlencode(parameters))

        response = urllib2.urlopen(url)
        html = response.read()

        response.close()

        return html
    def requestjson(self, path, parameters=[]):
        return json.loads(self.request(path, parameters))

    def updateoffset(self, offset):
        self.config.set('Telegram-Info', 'updates-offset', '0')

        with open('config.ini', 'wb') as configfile:
            self.config.write(configfile)

    def _updatethread(self):
        # Get updates.
        updates_json = self.requestjson('getUpdates', {'offset' : self.offset})

        if updates_json['ok']:
            for item in updates_json['result']:
                message = item['message']
                message_text = message['text']

                sender = message['from']

                sender_username = sender['username']
                sender_id       = sender['id']

                commands_tmp    = message_text.split(' ')

                command         = commands_tmp[0]

                command_body    = ''

                if len(commands_tmp) > 1:
                    command_body    = message_text[len(command)+1:]

                if 'download' == command:
                    self.downloadFile(command_body, sender_id)

                # Update offset
                self.offset = item['update_id'] + 1
                self.updateoffset(self.offset)

        threading.Timer(2.0, self._updatethread).start()

    def updatetask(self):
        if self.config.has_option('Telegram-Info', 'updates-offset'):
            self.offset = int(self.config['Telegram-Info']['updates-offset'])
        else:
            self.updateoffset(0)
            self.offset = 0

        self._updatethread()


    def sendMessage(self, user_id, message):
        self.request('sendMessage', {'chat_id' : user_id, 'text': message})


    def downloadFile(self, url, sender_id):
        file_name = self.config['Telegram-Info']['download-path'] + url.split('/')[-1]
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        self.sendMessage(sender_id, "Downloading: %s Bytes: %s" % (file_name, file_size))
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

        self.sendMessage(sender_id, "Download completed: %s" % (file_name))
        f.close()
