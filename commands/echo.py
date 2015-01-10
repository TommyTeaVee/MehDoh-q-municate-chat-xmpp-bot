__author__ = 'igorkhomenko'

import commands

class EchoCommand(commands.Command):
    __COMMAND_NAME__ = "echo"

    def __init__(self):
        self.command = EchoCommand.__COMMAND_NAME__
        self.description = "echoes the provided text"
        self.example_usage = "echo <text>"

    def process(self, message, xmpp_client):
        from_jid, command_argument = commands.Command.process(self, message, xmpp_client)

        # send the result of a command processing
        #
        xmpp_client.send_private_msg(command_argument, from_jid)