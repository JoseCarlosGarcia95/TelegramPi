class TelegramModule:

    """
    Retrieve information from Telegram API.
    """
    def __init__(self, Telegram):
        self.telegram = Telegram

    """
    Call the command handler.
    """
    def processCommand(self, command_body, sender_id):
        raise NotImplementedError('Process command not implemented')

    """
    Separate command body by ' '
    """
    def splitbody(self, command_body):
        return command_body.split(' ')
