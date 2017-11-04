from telegrampi.modules.TelegramModule import TelegramModule

import threading, urllib2
class DownloadFile(TelegramModule):

    def __init__(self, Telegram):
        TelegramModule.__init__(self, Telegram)
        self.permissionlevel = 7
        
    """
    Process the telegram response.
    """
    def processCommand(self, command_body, sender_id):
        # Default configuration
        self.useragent = ''
        self.cookies = ''
        self.downloading = False
        self.downloadthread = None

        # Command actions
        arguments = self.splitbody(command_body)
        action    = arguments[0]

        actions   = dict()

        actions['cancel']  = self.canceldownload
        actions['cookies'] = self.setcookies
        actions['browser'] = self.setbrowser

        if action in actions.keys():
            actions[action](command_body, arguments, sender_id)
        else:
            self.downloadfile(action, sender_id)


    """
    Cancel the current download.
    """
    def canceldownload(self, command_body, arguments, sender_id):
        if self.downloading:
            self.telegram.sendMessage(sender_id, 'Cancelling the current download')
            self.downloading = False

    """
    Set cookies if you want to download an authenticated download.
    """
    def setcookies(self, command_body, arguments, sender_id):
        if len(arguments) != 2:
            self.telegram.sendMessage(sender_id, 'Two arguments needed')
        else:
            self.cookies = arguments[1]

    """
    If you need a specify browser.
    """
    def setbrowser(self, command_body, arguments, sender_id):
        if len(arguments) != 2:
            self.telegram.sendMessage(sender_id, 'Two arguments needed')
        else:
            self.useragent = arguments[1]

    """
    Clear the current file name.
    """
    def clearfilename(self, url):
        filename = ''

        urlparts = url.split('/')
        filename = urlparts[-1]

        # Delete arguments.
        filename = filename.split('?')[0]

        return filename

    """
    Download file by url.
    """
    def downloadfile(self, file_to_download, sender_id):
        download_path = self.telegram.config['Modules']['download-file-path']

        filename      = self.clearfilename(file_to_download)

        self.telegram.sendMessage(sender_id, 'Downloading ' + filename)

        if self.downloading:
            self.telegram.sendMessage(sender_id, 'Download in process, please try again')
        else:
            self.downloading = True
            self.downloadthread = threading.Thread(target=self.downloadmanager, args=(download_path + filename, file_to_download, sender_id))
            self.downloadthread.start()

    """
    Start a download manager.
    """
    def downloadmanager(self, local_path, url, sender_id):
        headers = {'User-Agent' : self.useragent, 'Cookies' : self.cookies}

        req = urllib2.Request(url, None, headers)
        try:
            url_object = urllib2.urlopen(req)
        except:
            self.telegram.sendMessage(sender_id, 'Cannot download the specify file')
            return

        local_file = open(local_path, 'wb')
        meta_info  = url_object.info()
        file_size = int(meta_info.getheaders('Content-Length')[0])

        self.telegram.sendMessage(sender_id, "Downloading: %s kb: %s" % (url, file_size / 1024))

        file_size_dl = 0
        block_sz = 8192

        while self.downloading:
            buffer = url_object.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            local_file.write(buffer)

        if self.downloading:
            self.telegram.sendMessage(sender_id, "Download completed: %s" % (local_path))
            self.downloading = False
        else:
            self.telegram.sendMessage(sender_id, 'Download sucesfully cancelled')

        local_file.close()
