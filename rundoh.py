#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'igorkhomenko'

import sleekxmpp

import commands
import utils

import logging
logging.basicConfig()

config = {"app_id": "12496",
          "user_id": "2118126",
          "user_password": "mehdoh00",
          "dialog_id": "5474a58d535c12b4f9002b34"}

user_jid = config["user_id"] + "-" + config["app_id"] + "@chat.quickblox.com/macbookpro"
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

    def send_group_msg(self, text="testing"):
        new_message = self.make_message(mto=room_jid,
                      mbody=text,
                      mtype='groupchat')

        utils.add_extra_params(new_message)

        utils.log("SND: " + str(new_message))

        new_message.send()

    def send_private_msg(self, text="testing", to=None):
        new_message = self.make_message(mto=to,
                      mbody=text,
                      mtype='chat')

        utils.add_extra_params(new_message)

        utils.log("SND: " + str(new_message))

        new_message.send()

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

        utils.log("logged in")

        self.send_presence()

        # self.plugin['xep_0045'].joinMUC(self.room,
        #                                 self.nick,
        #                                 maxhistory="1",
        #                                 # If a room password is needed, use:
        #                                 # password=the_room_password,
        #                                 wait=True)

    def message(self, msg):
        if msg['type'] == "groupchat":
            return

        # Ignore messages from offline storage, track only real time messages
        delay_element  = msg.xml.find('{urn:xmpp:delay}delay')
        if delay_element is not None:
            return


        utils.log("RCV: " + str(msg))

        from_jid = msg['from']

        # try to extract command
        body = msg['body']

        potential_command = commands.extract_potential_command(body)

        # trying to find a command
        #
        try:
            command = commands.__COMMANDS_DICTIONARY__[potential_command]
        except KeyError:
             # there is no such command
             #
            text = "Hey! Available commands are: " + ','.join(commands.__COMMANDS_DICTIONARY__.keys()) + ". To get an example of the command usage enter 'help <command>'"
            self.send_private_msg(text, from_jid)
        else:
            command.process(msg, self)


    def muc_message(self, msg):

        # Ignore messages from offline storage, track only real time messages
        delay_element  = msg.xml.find('{urn:xmpp:delay}delay')
        if delay_element is not None:
            return

        utils.log(msg)


    def muc_online(self, presence):
        utils.log("RCV:" + str(presence))

        ujid = str(presence["muc"]["jid"])
        ptype = presence["type"]

        if config["user_id"] in ujid and ptype is "available":
            utils.log("joined room")

            self.send_group_msg(config["dialog_id"])


if __name__ == '__main__':
    utils.log("starting...")

    room_nick = config["user_id"]

    # Setup the MehDohBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = MehDohBot(user_jid, config["user_password"], room_jid, room_nick)
    xmpp.register_plugin('xep_0045') # Multi-User Chat

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        utils.log("connected")
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        #     ...
        xmpp.process(block=True)
        utils.log("Done")
    else:
        utils.log("Unable to connect.")