#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'igorkhomenko'

# 'list' - returns all commands. Example: 'list' - will return 'list, echo'
# 'echo' - echoes current message. Example: 'echo hello amigo' - will return 'hello amigo' back
#
__ECHO_COMMAND__ = "echo"
__COMMANDS_LIST__ = [__ECHO_COMMAND__]

def extract_potential_command(msg_text):
    body_split = msg_text.split(" ")
    if len(body_split) > 0:
        potential_command = body_split[0]
        return potential_command
