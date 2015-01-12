MehDoh! Q-municate Chat XMPP bot
===============

# Overview
Extensible XMPP Chat bot which works with https://qm.quickblox.com 

# Commands set
Bot has its own command set. To list all available commands just send something to bot. It will answer with a list of available commands.

To get an example of the command usage enter  **help 'command'**

# Write new command
All the commands are available as a part of **commands** module.
To write new comamnd follow next steps:

1. Create a new python file with a single class inherited from **commands.Command** and put this file inside the **commands** folder.
2. Set the variable **__COMMAND_NAME__** to command's name
3. Define the **__init__** method and set 3 fields inside: **command, description, example_usage**
4. Define the **process** method. This method defines the behaviour if a new command. 
5. Go to **__init__.py** file inside the **commands** folder and add your new command to **__COMMANDS_DICTIONARY__** variable.

# How to run
Use next command to run a bot:
```bash
nohup python rundoh.py &
```

Sometimes it's useful to automatically run a script on a Linux when it boots up.
I prepared the **init.d** script which can be used to manage to MehDoh bot.
First of all copy it to **/etc/init.d/** directory on your Linux.

Then make the script executable:
```bash
sudo chmod +x /etc/init.d/mehdoh
```

Next you can start the mehdoh bot with this command:
```bash
sudo /etc/init.d/mehdoh start
```

...and stop it again with this one:
```bash
sudo /etc/init.d/mehdoh stop
```

In order to make the bot run on start up, it's necessary to run this command:
```bash
sudo update-rc.d mehdoh defaults
```

This creates a link to /etc/init.d/mehdoh in directories from /etc/rc0.d through to /etc/rc6.d. When Linux boots up or shuts down, it looks in these folders to see if any scripts or programs need to be run. When I restart my laptop the mehdoh bot starts automatically.

# Live demo
Here is a live working bot on https://qm.quickblox.com. Go to search box and add the user with name **mehdoh** to contacts. After that you can try to use available commands.
