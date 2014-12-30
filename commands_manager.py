#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'igorkhomenko'

import utils

class Command:
    def __init__(self):
        self.command = None
        self.description = None
        self.example_usage = None

    def get_description(self):
        return self.description

    def example_usage(self):
        return self.example_usage

    def process(self, message, xmpp_client):
        body = message['body']
        global from_jid
        from_jid = message['from']
        global dialog_id
        dialog_id = utils.extract_dialog_id(message)
        global command_argument
        command_argument = body.replace(self.command + " ", "", 1)

    def __str__(self):
        return self.command

class PingCommand(Command):
    __COMMAND_NAME__ = "ping"

    def __init__(self):
        self.command = PingCommand.__COMMAND_NAME__
        self.description = "pings the bot"
        self.example_usage = "ping"

    def process(self, message, xmpp_client):
        Command.process(self, message, xmpp_client)

        # send the result of a command processing
        #
        xmpp_client.send_private_msg(dialog_id, "pong", from_jid)

class EchoCommand(Command):
    __COMMAND_NAME__ = "echo"

    def __init__(self):
        self.command = EchoCommand.__COMMAND_NAME__
        self.description = "echoes the provided text"
        self.example_usage = "echo <text>"

    def process(self, message, xmpp_client):
        Command.process(self, message, xmpp_client)

        # send the result of a command processing
        #
        xmpp_client.send_private_msg(dialog_id, command_argument, from_jid)

class HelpCommand(Command):
    __COMMAND_NAME__ = "help"

    def __init__(self):
        self.command = HelpCommand.__COMMAND_NAME__
        self.description = "provides an example how to use a particular command"
        self.example_usage = "help <command>"

    def process(self, message, xmpp_client):
        Command.process(self, message, xmpp_client)


        command_to_help = command_argument.split(' ')[0]

        result = None
        try:
            command_to_help_obj = __COMMANDS_DICTIONARY__[command_to_help]
        except KeyError:
            result = "Sorry pal, command '" + command_to_help + "' not found"
        else:
            result = "'" + command_to_help + "' command " + command_to_help_obj.description + ". Usage: " + command_to_help_obj.example_usage

        # send the result of a command processing
        #
        xmpp_client.send_private_msg(dialog_id, result, from_jid)


__COMMANDS_DICTIONARY__ = {PingCommand.__COMMAND_NAME__: PingCommand(),
                           EchoCommand.__COMMAND_NAME__: EchoCommand(),
                           HelpCommand.__COMMAND_NAME__: HelpCommand()}

def extract_potential_command(msg_text):
    body_split = msg_text.split(" ")
    if len(body_split) > 0:
        potential_command = body_split[0]
        return potential_command