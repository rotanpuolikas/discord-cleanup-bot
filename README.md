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

The bot is configured with environment variables The easiest way is to use a `.env`file (dotenv style).

Create a `.env` file using the provided `.env.example` to the same directory as `bot.py` and edit it.

```sh
cp .env.example .env
```

### Supported environment variables

- **CLEANUP_WAIT** sets the amount of hours between each cleanup task loop (default: 1)
- **DELETE_AFTER_DAYS** sets the limit as to when a message should be deleted or saved (default: 3)
- **DELETE_DELAY** sets the delay between message deletions (in seconds), should be 1 at minimum to avoid rate limiting (default: 1.2)
- **FETCH_LIMIT** sets the amount of messages fetched per cleanup loop run (default: 200)
- **CONFIG_FILE** sets the file where the configured channels are saved (default: ./data/channels.json)
- **TOKEN** bot token as string
- **TOKENFILE** path to a file containing the bot token (default: ./data/discord_token)

The bot uses TOKEN if set, otherwise it uses TOKENFILE.

## Setup

1. Create the bot at Discord Developer portal
2. "Installation" -tab

   - Install Link: None

3. "Bot" -tab

   - Public Bot: No / Uncheck
   - Message Content Intent: Yes / Check

4. "OAuth2" -tab:

   - Scopes:
     - bot
     - applications.commands
   - Bot permissions:
     - General Permissions: View Channels
     - Text Permissions: Manage Messages
     - Text Permissions: Read Message History

5. Open the generated Oauth2 URL at the bottom of the page and invite the bot to the desired server
6. Invite the bot/role to the desired channel
7. Add the channel to the bot with `/channel_add`

The next part is to setup whatever you run the bot on, this works on Debian 13.

1. Install python, minimum 3.9, newest recommended
2. Install dependencies (pip install -r requirements.txt)
3. Start the bot with python3 bot.py
4. Optionally create a fancy schmancy script to start the bot at system startup

If you prefer using Docker, you can use the included files with e.g. Docker compose:

```sh
docker compose up -d --build
```

## startbot.sh

It is HIGHLY recommended to NOT run discord bots as the root user.

This is my autostartup script, it is located somewhere in the depths of the system, it has a couple of configurable options:

**USER_NAME** is the name of the UNPRIVILEGED user running the bot

**SESSION_NAME** is the name of the screen session that runs the bot

**PYTHON_SCRIPT** is where the bot.py file is located

**WORKDIR** is the working directory (for screen)

Basically you need to create a systemd service (or whichever service manager you use), and make it run this script at startup. Simple as.
