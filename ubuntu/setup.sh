#!/bin/bash

PORT=""
DISCORD_UID=""
# Check if both arguments are provided

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <PORT> <DISCORD_UID>"
  exit 1
elif [[ $1 =~ ^[0-9]+$ ]]; then
    PORT=$1
    DISCORD_UID=$2
else
    PORT=$2
    DISCORD_UID=$1
fi 

echo "The port is: $PORT"
echo "Discord_UID is: $DISCORD_UID"

# Set up sandcat-agent
echo "Setting up sandcat-agent"
server="http://host.docker.internal:$PORT";

curl -s -X POST -H "file:sandcat.go" -H "platform:linux" "$server/file/download" > "$DISCORD_UID";
chmod +x "$DISCORD_UID";
./"$DISCORD_UID" -server "$server" -v
