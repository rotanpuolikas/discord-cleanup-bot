## Discord channel cleanup bot

This bot cleans up Discord message channels. You need to have channel managing permissions to use this bot. I am not hosting this bot, you have to host it yourself.

This bot comes with no warranty, don't blame me for not reading through the code and accidentally deleting all messages on your entire Discord server.

## Usage

The bot automatically checks all configured channels every 1 hour (can be changed), and deletes messages older than 3 days (can also be changed).

When adding a channel, the bot does not immediately start deleting messages on that channel, it waits until the next time the deletion job runs. You can restart the bot to immediately start deleting messages on the configured channels.

Manage channels on the cleanup list via these commands:

**/channel_add** adds a channel to the cleanup list

**/channel_remove** removes a channel from the cleanup list

**/channel_list** lists all channels being cleaned up

## Configuration

At the top of the bot.py, there are a couple of configurable options:

**CLEANUP_WAIT** sets the amount of hours between each cleanup task loop

**DELETE_AFTER_DAYS** sets the limit as to when a message should be deleted or saved

**DELETE_DELAY** sets the delay between message deletions (in seconds), should be 1 at minimum to avoid rate limiting

**FETCH_LIMIT** sets the amount of messages fetched per cleanup loop run

**CONFIG_FILE** sets the file where the configured channels are saved

**TOKENFILE** is optional, you can also use

**TOKEN** which is the bot token.

If you decide to hard-code the **TOKEN**, be sure to remove or comment out
```py
with open(TOKENFILE, "r") as tokenfile:
    TOKEN = tokenfile.read().strip()
  
```

## Setup

1. Create the bot at Discord Developer portal
2. On the "Installation" -tab, select "None" as the install link
3. At the "Bot" -tab, uncheck "Public Bot", and check "Message Content Intent"
4. Create the OAuth2 invite link on the "OAuth2" -tab, and select these:
"Scopes":
bot, applications.commands
"Bot permissions":
View Channels, Manage Messages, Read Message History
5. Use the generated URL at the bottom of the page to invite the bot to the desired server

The next part is to setup whatever you run the bot on

1. Install python, minimum 3.9, newest recommended
2. Install the discord package via pip (pip install discord)
3. Start the bot with python3 bot.py
4. Optionally create a fancy schmancy script to start the bot at system startup

## startbot.sh

It is HIGHLY recommended to NOT run discord bots as the root user.

This is my autostartup script, it is located somewhere in the depths of the system, it has a couple of configurable options:

**USER_NAME** is the name of the UNPRIVILEGED user running the bot

**SESSION_NAME** is the name of the screen session that runs the bot

**PYTHON_SCRIPT** is where the bot.py file is located

**WORKDIR** is the working directory (for screen)

Basically you need to create a systemd service (or whichever service manager you use), and make it run this script at startup. Simple as.
