#!/bin/bash

#set up manx-agent
    echo "Setting up manx-agent"
    server="http://127.0.0.1:58288"
    socket="127.0.0.1:58210"
    #contact="tcp"
    
    curl -s -X POST -H "file:manx.go" -H "platform:linux" $server/file/download > manx;
    chmod +x manx;
    ./manx -http $server -socket $socket -contact tcp -v


