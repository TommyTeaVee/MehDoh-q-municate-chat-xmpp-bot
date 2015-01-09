__author__ = 'igorkhomenko'

import commands

class PingCommand(commands.Command):
    __COMMAND_NAME__ = "ping"

    def __init__(self):
        self.command = PingCommand.__COMMAND_NAME__
        self.description = "pings the bot"
        self.example_usage = "ping"

    def process(self, message, xmpp_client):
        from_jid, dialog_id, command_argument = commands.Command.process(self, message, xmpp_client)

        # send the result of a command processing
        #
        xmpp_client.send_private_msg(dialog_id, "pong", from_jid)