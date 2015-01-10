MehDoh! Q-municate Chat XMPP bot
===============

# How to run
Use next command to run a bot:
```bash
nohup python rundoh.py &
```

Sometimes it's useful to automatically run a script on a Pi when it boots up.
I prepared the **init.d** script which can be used to manage to MehDoh bot.
First of all copy it to **/etc/init.d/** directory on your Pi.

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

This creates a link to /etc/init.d/mehdoh in directories from /etc/rc0.d through to /etc/rc6.d. When Linux boots up or shuts down, it looks in these folders to see if any scripts or programs need to be run. When I restart my Pi the servod program starts automatically.
