#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'igorkhomenko'

class Command:
    def __init__(self):
        self.command = None
        self.description = None
        self.example_usage = None

    def get_description(self):
        return self.description

    def example_usage(self):
        return self.example_usage

class PingCommand(Command):
    __COMMAND__ = "ping"

    def __init__(self):
        self.command = "ping"
        self.description = "Pings the bot."
        self.example_usage = "ping"

class EchoCommand(Command):
    __COMMAND__ = "echo"

    def __init__(self):
        self.description = "Echoes the provided text."
        self.example_usage = "echo <text>"

class HelpCommand(Command):
    __COMMAND__ = "help"

    def __init__(self):
        self.description = "Provides an example how to use a particular command."
        self.example_usage = "help <command>"


__COMMANDS_LIST__ = [PingCommand.__COMMAND__, EchoCommand.__COMMAND__, HelpCommand.__COMMAND__]


def extract_potential_command(msg_text):
    body_split = msg_text.split(" ")
    if len(body_split) > 0:
        potential_command = body_split[0]
        return potential_command