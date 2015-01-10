#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'igorkhomenko'

__DEBUG__ = False

from sleekxmpp.xmlstream import ET
import time

def add_extra_params(msg):
    """
    Adds 'extraParams' to a message
    """

    extra_params_out = ET.Element('{jabber:client}extraParams')
    #
    date_sent_out = ET.Element('{}date_sent')
    date_sent_out.text = str(int(time.time()))
    extra_params_out.append(date_sent_out)
    #
    save_to_history_out = ET.Element('{}save_to_history')
    save_to_history_out.text = "1"
    extra_params_out.append(save_to_history_out)

    msg.append(extra_params_out)

def log(str):
    if __DEBUG__:
        print(str)