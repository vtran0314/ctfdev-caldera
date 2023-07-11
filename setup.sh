#!/bin/bash
PORT = ""
DISCORD_UID = ""

IFS=" " real -p "Input port and discord's uid: " PORT DISCORD_UID 
    
#set up sandcat-agent
echo "Setting up sandcat-agent"
server="http://host.docker.internal:${PORT}"

curl -s -X POST -H "file:sandcat.go" -H "platform:linux" $server/file/download > ${DISCORD_UID};
chmod +x DICORD_UID;
./DISCORD_UID -server $server -v
