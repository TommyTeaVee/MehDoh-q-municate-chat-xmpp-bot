__author__ = 'igorkhomenko'

import utils

class Command:
    def __init__(self):
        self.command = None
        self.description = None
        self.example_usage = None

    def process(self, message, xmpp_client):
        body = message['body']
        from_jid = message['from']
        dialog_id = utils.extract_dialog_id(message)
        command_argument = body.replace(self.command + " ", "", 1)
        return (from_jid, dialog_id, command_argument)

    def __str__(self):
        return self.command

def extract_potential_command(msg_text):
    body_split = msg_text.split(" ")
    if len(body_split) > 0:
        potential_command = body_split[0]
        return potential_command


from . import echo, help, ping
__COMMANDS_DICTIONARY__ = {echo.EchoCommand.__COMMAND_NAME__: echo.EchoCommand(),
                           help.HelpCommand.__COMMAND_NAME__: help.HelpCommand(),
                           ping.PingCommand.__COMMAND_NAME__: ping.PingCommand()}