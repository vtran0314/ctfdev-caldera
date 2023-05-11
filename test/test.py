import socket
import random
import re
import os
import shutil
import subprocess
#from flask import Flask

#app = Flask(__name__)
#@app.route('/check-port')

WORK_DIR = subprocess.check_output('pwd').decode('utf-8').strip()


def prep_caldera_server():
    global CALDERA_SERVER_STATUS
    CALDERA_SERVER_STATUS = False
    # Check if the ctf-servers directory exists
    if not os.path.isdir('ctf-servers'):
        os.mkdir('ctf-servers')
        
    # Get a list of existing server directories and their numbers
    server_dirs = os.listdir('ctf-servers')
    server_nums = [int(d.split('_')[1]) for d in server_dirs if d.startswith('server_')]
    
    # If no server directory exists, create the first one
    if len(server_nums) == 0:
        next_num = 1
        next_dir = f'server_{next_num}'
        os.mkdir(os.path.join('ctf-servers', next_dir))
        
    # If server directories exist, find the next available number and create the directory
    else:
        next_num = max(server_nums) + 1
        next_dir = f'server_{next_num}'
        os.mkdir(os.path.join('ctf-servers', next_dir))
    
    # # Copy the caldera_server folder into the new server directory
    shutil.copytree('caldera_server', os.path.join('ctf-servers', next_dir, 'caldera-server'))
    
    # # Copy the default.yml file to the new server directory
    shutil.copy('default.yml', os.path.join('ctf-servers', next_dir, 'caldera-server', 'conf', 'default.yml'))

    # Start the caldera server
    server_path = os.path.join("ctf-servers", next_dir, "caldera-server")
    os.chdir(server_path)
    #os.system('pwd')
    cmd = "python3 server.py --insecure"
    #subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    #print("Running process")
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Use communicate to read the output from the subprocess
    while True:
        output = process.stderr.readline().decode('utf-8').strip()
        #print(output)
        if output == '' and process.poll() is not None:
            break
        if 'All systems ready.' in output:
            CALDERA_SERVER_STATUS = True
            return CALDERA_SERVER_STATUS
    
    return CALDERA_SERVER_STATUS
    
def prep_docker_ubuntu(http, tcp):
    
    #print("prep_docker_ubuntu..........")
    os.chdir(WORK_DIR)
    #os.system('pwd')

    #print("modifying setup.sh file")
    with open('./ubuntu/setup.sh', 'r') as f:
        file_str = f.read()

    patterns = [
        (r'server\s*=\s*.*$', f'server="http://127.0.0.1:{http}"'),
        (r'socket\s*=\s*.*$', f'socket="127.0.0.1:{tcp}"') 
    ]

    for pattern, replacement in patterns:
        file_str = re.sub(pattern, replacement, file_str, flags=re.MULTILINE)

#Write the modified string back to the setup.sh file
    with open('./ubuntu/setup.sh', 'w') as f:
        f.write(file_str)

    #print("Done!!!!")

    #print("modifying Dockerfile................")
    with open('./ubuntu/Dockerfile', 'r') as f:
        file_str = f.read()

    patterns = [
        (r'EXPOSE\s.*$', f'EXPOSE {http}') 
    ]   

    for pattern, replacement in patterns:
        file_str = re.sub(pattern, replacement, file_str, flags=re.MULTILINE)

    # Write the modified string back to the setup.sh file
    with open('./ubuntu/Dockerfile', 'w') as f:
        f.write(file_str)
    
    dockerImages = subprocess.check_output(['docker', 'images', '-a']).decode('utf-8')
    ##print(dockerImages)

    dockerImages_nums = [
        int(re.search(r'^ubuntuimages-(\d+)', d).group(1))
        for d in dockerImages.split('\n')
        if re.match(r'^ubuntuimages-\d+', d)
    ]
    # dockerImages_nums = [int(d.split('-')[1]) for d in dockerImages.split('\n') if re.match(r'ubuntuimages-\d+', d)]

    # dockerImages_nums = [int(d.split('-')[1]) for d in dockerImages.split('\n') if d.startswith('ubuntuimages-')]
    #print(dockerImages_nums)
    if len(dockerImages_nums) == 0:
        next_num = 1
        next_img = f'ubuntuimages-{next_num}'
        dockerBuild = f'docker build -t {next_img}:latest ./ubuntu/'
        #print(dockerBuild)
        subprocess.Popen(dockerBuild.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()

        dockerRun = f'docker run -d {next_img}:latest'
        #print(dockerRun)
        subprocess.run(dockerRun.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    else:
        next_num = max(dockerImages_nums) + 1
        next_img = f'ubuntuimages-{next_num}'
        dockerBuild = f'docker build -t {next_img}:latest ./ubuntu/'
        #print(dockerBuild)
        subprocess.Popen(dockerBuild.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()

        dockerRun = f'docker run -d {next_img}:latest'
        #print(dockerRun)
        subprocess.run(dockerRun.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def check_port():
    OPEN_PORT = []
    PORT = 0
    
    for port in range(1, 65536):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex(('localhost', port))
            if result == 0:
                OPEN_PORT.append(port)
            sock.close()
        except:
            pass

    while True:
        PORT = random.randint(300, 650) * 100
        if PORT not in OPEN_PORT:
            break
        
    with open('default.yml', 'r') as f:
        file_str = f.read()
    
    DNS_PORT= PORT + 53
    HTTP_PORT = PORT + 88
    SSH_PORT = PORT + 222
    FTP_PORT = PORT + 22
    TCP_PORT = PORT + 10
    UDP_PORT = PORT + 11
    WS_PORT = PORT + 12

    patterns = [
        (r'^app\.contact\.dns\.socket:.*$', f'app.contact.dns.socket: 127.0.0.1:{DNS_PORT}'),
        (r'^app\.contact\.http:.*$', f'app.contact.http: http://127.0.0.1:{HTTP_PORT}'),
        (r'^app\.contact\.tunnel\.ssh\.socket:.*$', f'app.contact.tunnel.ssh.socket: 127.0.0.1:{SSH_PORT}'),
        (r'^app\.contact\.ftp\.port:.*$', f'app.contact.ftp.port: {FTP_PORT}'),
        (r'^app\.contact\.tcp:.*$', f'app.contact.tcp: 127.0.0.1:{TCP_PORT}'),
        (r'^app\.contact\.udp:.*$', f'app.contact.udp: 127.0.0.1:{UDP_PORT}'),
        (r'^app\.contact\.websocket:.*$', f'app.contact.websocket: 127.0.0.1:{WS_PORT}'),
        (r'^port:.*$', f'port: {HTTP_PORT}')
    ]

    # Use a loop to find and replace each line that matches the regular expression
    for pattern, replacement in patterns:
        file_str = re.sub(pattern, replacement, file_str, flags=re.MULTILINE)

    # Write the modified string back to the default.yml file
    with open('default.yml', 'w') as f:
        f.write(file_str)
    
    #prepare server
    prep_caldera_server()
    if CALDERA_SERVER_STATUS == True:
        #print("Starting Docker.....")
        prep_docker_ubuntu(HTTP_PORT, TCP_PORT)
    else:
        exit()
    
    return str(HTTP_PORT)

print(check_port())
