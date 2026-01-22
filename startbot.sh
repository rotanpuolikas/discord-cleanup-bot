#!/bin/bash

USER_NAME="botti"
SESSION_NAME="python"
PYTHON_SCRIPT="/home/botti/bot.py"
WORKDIR="/home/botti"

# ensure HOME is set correctly
export HOME="/home/${USER_NAME}"
cd "$WORKDIR" || exit 1

# start screen session only if it doesn't already exist
/usr/bin/screen -list | grep -q "\.${SESSION_NAME}" || \
/usr/bin/screen -dmS "$SESSION_NAME" /usr/bin/python3 "$PYTHON_SCRIPT"
