#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'igorkhomenko'


import sleekxmpp
from sleekxmpp.xmlstream import ET

import commands_manager

import logging
logging.basicConfig()

config = {"app_id": "12496",
          "user_id": "2015753",
          "user_password": "mehdoh00",
          "dialog_id": "5474a58d535c12b4f9002b34"}

user_jid = config["user_id"] + "-" + config["app_id"] + "@chat.quickblox.com"
room_jid = config["app_id"] + "_" + config["dialog_id"] + "@muc.chat.quickblox.com"


class MehDohBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, room, nick):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.room = room
        self.nick = nick

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        # The groupchat_message event is triggered whenever a message
        # stanza is received from any chat room. If you also also
        # register a handler for the 'message' event, MUC messages
        # will be processed by both handlers.
        self.add_event_handler("groupchat_message", self.muc_message)

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler("message", self.message)

        # The groupchat_presence event is triggered whenever a
        # presence stanza is received from any chat room, including
        # any presences you send yourself. To limit event handling
        # to a single room, use the events muc::room@server::presence,
        # muc::room@server::got_online, or muc::room@server::got_offline.
        self.add_event_handler("muc::%s::got_online" % self.room,
                               self.muc_online)

    def send_group_msg(self, dialog_id, text="testing"):
        new_message = self.make_message(mto=room_jid,
                      mbody=text,
                      mtype='groupchat')

        extra_params_out = ET.Element('{jabber:client}extraParams')
        #
        dialog_id_out = ET.Element('{}dialog_id')
        dialog_id_out.text = dialog_id
        extra_params_out.append(dialog_id_out)
        #
        save_to_history_out = ET.Element('{}save_to_history')
        save_to_history_out.text = "1"
        extra_params_out.append(save_to_history_out)
        #
        new_message.append(extra_params_out)

        print("sending a group message: " + str(new_message))

        new_message.send()

    def send_private_msg(self, dialog_id, text="testing", to=None):
        new_message = self.make_message(mto=to,
                      mbody=text,
                      mtype='chat')

        extra_params_out = ET.Element('{jabber:client}extraParams')
        #
        dialog_id_out = ET.Element('{}dialog_id')
        dialog_id_out.text = dialog_id
        extra_params_out.append(dialog_id_out)
        #
        save_to_history_out = ET.Element('{}save_to_history')
        save_to_history_out.text = "1"
        extra_params_out.append(save_to_history_out)
        #
        new_message.append(extra_params_out)

        print("sending a private message: " + str(new_message))

        new_message.send()

    def extract_dialog_id(self, message):
        """
        Extract a dialog_id from a message
        """
        dialog_id_in = message.xml.find('{jabber:client}extraParams/{jabber:client}dialog_id')
        return dialog_id_in.text

    def start(self, event):
        """
        Process the session_start event.
        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.
        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        #self.get_roster()
        print("logged in")

        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        maxhistory="1",
                                        # If a room password is needed, use:
                                        # password=the_room_password,
                                        wait=True)

    def message(self, msg):
        print(msg)

        from_jid = msg['from']

        # try to extract command
        body = msg['body']
        body_split = body.split(" ")
        if len(body_split) > 0:
            potential_command = body_split[0]

            print(potential_command)

            index = None
            try:
                index = commands_manager.__COMMANDS_LIST__.index(potential_command)
            except ValueError:
                pass
            else:
                dialog_id = self.extract_dialog_id(msg)
                print(dialog_id)
                if potential_command == commands_manager.__LIST_COMMAND__:
                    text = "Hey! Available commands are: " + ','.join(commands_manager.__COMMANDS_LIST__)
                    self.send_private_msg(dialog_id, text, from_jid)
                elif potential_command == commands_manager.__ECHO_COMMAND__:
                    text = ' '.join(body_split[1:])
                    self.send_private_msg(dialog_id, text, from_jid)
                    pass




    def muc_message(self, msg):
        #
        # Ignore messages from offline storage, track only real time messages
        #
        delay_element  = msg.xml.find('{urn:xmpp:delay}delay')
        if delay_element is not None:
            return

        print(msg)


    def muc_online(self, presence):
        print("RCV:" + str(presence))

        ujid = str(presence["muc"]["jid"])
        ptype = presence["type"]

        if config["user_id"] in ujid and ptype is "available":
            print("joined room")
            self.send_group_msg(config["dialog_id"])


if __name__ == '__main__':
    print("starting...")

    room_nick = config["user_id"]

    # Setup the MehDohBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = MehDohBot(user_jid, config["user_password"], room_jid, room_nick)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0045') # Multi-User Chat
    xmpp.register_plugin('xep_0199') # XMPP Ping

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        print("connected")
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        #     ...
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")