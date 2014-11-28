#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'igorkhomenko'

from sleekxmpp.xmlstream import ET

def extract_dialog_id(message):
    """
    Extracts a dialog_id from a message
    """

    dialog_id_in = message.xml.find('{jabber:client}extraParams/{jabber:client}dialog_id')
    return dialog_id_in.text

def add_extra_params(msg, dialog_id):
    """
    Adds 'extraParams' to a message
    """

    extra_params_out = ET.Element('{jabber:client}extraParams')
    #
    dialog_id_out = ET.Element('{}dialog_id')
    dialog_id_out.text = dialog_id
    extra_params_out.append(dialog_id_out)
    #
    save_to_history_out = ET.Element('{}save_to_history')
    save_to_history_out.text = "1"
    extra_params_out.append(save_to_history_out)

    msg.append(extra_params_out)