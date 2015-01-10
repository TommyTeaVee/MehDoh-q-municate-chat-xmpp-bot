__author__ = 'igorkhomenko'

import commands

class HelpCommand(commands.Command):
    __COMMAND_NAME__ = "help"

    def __init__(self):
        self.command = HelpCommand.__COMMAND_NAME__
        self.description = "provides an example how to use a particular command"
        self.example_usage = "help <command>"

    def process(self, message, xmpp_client):
        from_jid, command_argument = commands.Command.process(self, message, xmpp_client)


        command_to_help = command_argument.split(' ')[0]

        result = None
        try:
            command_to_help_obj = commands.__COMMANDS_DICTIONARY__[command_to_help]
        except KeyError:
            result = "Sorry pal, command '" + command_to_help + "' not found"
        else:
            result = "'" + command_to_help + "' command " + command_to_help_obj.description + ". Usage: " + command_to_help_obj.example_usage

        # send the result of a command processing
        #
        xmpp_client.send_private_msg(result, from_jid)
