import discord
from discord.ext import commands, tasks
from discord import app_commands
import json
import os
import asyncio
from datetime import datetime, timedelta, timezone

# load environment variables from .env file if present
from dotenv import load_dotenv
load_dotenv()

# import logging
# logging.basicConfig(level=logging.INFO)
# logging.getLogger("discord").setLevel(logging.DEBUG)
# logging.getLogger("discord.http").setLevel(logging.DEBUG)

# configuration via environment variables, with sane defaults
CLEANUP_WAIT = int(os.getenv("CLEANUP_WAIT", "1"))  # hours
DELETE_AFTER_DAYS = int(os.getenv("DELETE_AFTER_DAYS", "3"))  # days
DELETE_DELAY = float(os.getenv("DELETE_DELAY", "1.2"))  # seconds
FETCH_LIMIT = int(os.getenv("FETCH_LIMIT", "200"))  # messages to fetch per loop, to avoid being rate limited
CONFIG_FILE = os.getenv("CONFIG_FILE", "./data/channels.json")

# either read bot token from a file (which i do) or just add the token like this:
TOKEN = os.getenv("TOKEN", "")
TOKENFILE = os.getenv("TOKENFILE", "./.discord_token")

if not TOKEN and TOKENFILE:
    with open(TOKENFILE, "r") as tokenfile:
        TOKEN = tokenfile.read().strip()

if not TOKEN:
    raise RuntimeError("No TOKEN set. Provide TOKEN or TOKENFILE.")

# discord bot shenanigans, dont touch

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# end of bot shenanigans


# cleanup channels load / save functions

def load_channels():
    if not os.path.exists(CONFIG_FILE):
        return []
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_channels(channels):
    with open(CONFIG_FILE, "w") as f:
        json.dump(channels, f)


# bot slash commands

@tree.command(name="channel_add", description="Enable autocleanup on a channel")
@app_commands.checks.has_permissions(manage_channels=True)
async def cleanup_add(interaction: discord.Interaction, channel: discord.TextChannel):
    channels = load_channels()

    if channel.id in channels:
        await interaction.response.send_message(f"{channel.mention} is already on the cleanup list", ephemeral=True)
        return

    channels.append(channel.id)
    save_channels(channels)
    await interaction.response.send_message(f"Added {channel.mention} to the cleanup list", ephemeral=True)


@tree.command(name="channel_remove", description="Disable autocleanup on a channel")
@app_commands.checks.has_permissions(manage_channels=True)
async def cleanup_remove(interaction: discord.Interaction, channel: discord.TextChannel):
    channels = load_channels()

    if channel.id not in channels:
        await interaction.response.send_message(f"{channel.mention} is not on the cleanup list", ephemeral=True)
        return

    channels.remove(channel.id)
    save_channels(channels)

    await interaction.response.send_message(f"Removed {channel.mention} from the cleanup list", ephemeral=True)


@tree.command(name="channel_list", description="List all channels currently on the cleanup list")
async def cleanup_list(interaction: discord.Interaction):
    channels = load_channels()

    if not channels:
        await interaction.response.send_message("No channels are currently on the cleanup list", ephemeral=True)
        return

    mentions = []
    for cid in channels:
        channel = bot.get_channel(cid)
        if channel:
            mentions.append(channel.mention)

    await interaction.response.send_message("Cleanup is enabled for: \n" + "\n".join(mentions), ephemeral=True)


# cleanup task
@tasks.loop(hours=CLEANUP_WAIT)
async def cleanup_task():
    channels = load_channels()

    if not channels:
        return

    cutoff = datetime.now(timezone.utc) - timedelta(days=DELETE_AFTER_DAYS)

    for channel_id in channels:
        channel = bot.get_channel(channel_id)

        if not isinstance(channel, discord.TextChannel):
            continue

        deleted = 0

        try:
            async for message in channel.history(limit=FETCH_LIMIT):
                if message.created_at > cutoff: # stop when reaching newer messages
                    continue

                try:
                    await message.delete()
                    deleted += 1
                    await asyncio.sleep(DELETE_DELAY)
                except discord.Forbidden:
                    print(f"No permission in {channel.name}")
                    break
                except discord.HTTPException: # rate limit or transient error
                    await asyncio.sleep(5)

        except Exception as e:
            print(f"Cleanup error in {channel_id}: {e}")

        if deleted:
            print(f"Deleted {deleted} messages in #{channel.name}")


# bot startup DONT TOUCH

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        cleanup_task.start()
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
        print(f"Cleanup task running every {CLEANUP_WAIT} hours")
    except Exception as e:
        print(f"Error at startup: {e}")


if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except KeyboardInterrupt:
        print("exiting")
    except Exception as e:
        print(f"Exception: {e}")
