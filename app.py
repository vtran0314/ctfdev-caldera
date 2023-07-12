import socket
import random
import re
import os
import shutil
import subprocess
import requests
import logging
import json
import pathlib
import settings
from flask import jsonify
#from flask import Flask, jsonify
#from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)
logger = settings.logging.getLogger(__name__)

class CalderaServer:
    def __init__(self):
        self.WORK_DIR = pathlib.Path(__file__).parent
        self.status = False
        self.next_dir = None

    def preparation(self):
        self.status = False
        self.create_sv_directory()
        self.copy_sv_directory()
        self.start()

    def create_sv_directory(self):
        if not os.path.isdir('ctf-servers'):
            os.mkdir('ctf-servers')

        server_dirs = os.listdir('ctf-servers')
        server_nums = [int(d.split('_')[1]) for d in server_dirs if d.startswith('server_')]

        if len(server_nums) == 0:
            next_num = 1
        else:
            next_num = max(server_nums) + 1

        self.next_dir = f'server_{next_num}'
        os.mkdir(os.path.join('ctf-servers', self.next_dir))

    def copy_sv_directory(self):
        shutil.copytree('caldera-lightweight', os.path.join('ctf-servers', self.next_dir, 'caldera-lightweight'))
        shutil.copy('caldera-lightweight/conf/default.yml', os.path.join('ctf-servers', self.next_dir, 'caldera-lightweight', 'conf', 'default.yml'))

    #Generate new API key by restart the caldera server without --fresh or --insecure flag. 
    #Also, ensure to remove the local.yml file
    def operation(self):
        url = f"http://0.0.0.0:{find_port.get_port}/api/v2/operations"
        headers = {
        'Content-Type': 'application/json',
        'KEY': 'FsZj64pZezhcHyZRS3QRg27xjY20J5ID7buaanRVwe4'
        }
        data = {
        'name': 'test',
        'group': 'red',
        'adversary': {'adversary_id': '01d77744-2515-401a-a497-d9f7241aac3c'},
        'auto_close': False,
        'state': 'running',
        'autonomous': 1,
        'planner': {'id': '788107d5-dc1e-4204-9269-38df0186d3e7'},
        'source': {'id': 'ed32b9c3-9593-4c33-b0db-e2007315096b'},
        'use_learning_parsers': True,
        'obfuscator': 'plain-text',
        'jitter': '2/8',
        'visibility': '51'}
        
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            logger.info('Request successful!')
            logger.info(response.json())
        else:
            logger.error('Request failed with status code: %d', response.status_code)


    def start(self):
        server_path = os.path.join("ctf-servers", self.next_dir, "caldera-lightweight")
        os.chdir(server_path)
        cmd = "python3 server.py --fresh --insecure"
        process = subprocess.Popen(cmd.split(), stderr=subprocess.PIPE, stdout=subprocess.DEVNULL)

        while True:
            output = process.stderr.readline().decode('utf-8').strip()
            logging.error(output)
            if output == '' and process.poll() is not None:
                break
            if 'All systems ready.' in output:
                self.status = True
                return self.status
            logging.error(self.status)
        return self.status

'''
To-do:
    *Check if docker exist.
    *Get discord UID from env file
    *Get docker id or docker name. 
'''
class UbuntuClient:
    def start_docker(self, port, discord_uid, DOCKER_ID):
        cmd = f'docker exec {DOCKER_ID} /usr/src/app/setup.sh {port} {discord_uid}'
        subprocess.run(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

class FindPort:
    def __init__(self):
        self.open_port = []
        self.port = 0

    def get_port(self):
        self.find_open_ports()
        self.generate_random_port()
        return self.set_config()


    def find_open_ports(self):
        for port in range(30000, 65536):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                result = sock.connect_ex(('localhost', port))
                if result == 0:
                    self.open_port.append(port)
                sock.close()
            except:
                pass

    def generate_random_port(self):
        while True:
            self.port = random.randint(300, 650) * 100
            if self.port not in self.open_port:
                break

    def set_config(self):
        
        config_file = settings.CALD_CONFIG_DIR / "default.yml"
        
        with open(config_file, 'r') as f:
            file_str = f.read()

        DNS_PORT = self.port + 53
        HTTP_PORT = self.port + 88
        SSH_PORT = self.port + 222
        FTP_PORT = self.port + 22
        TCP_PORT = self.port + 10
        UDP_PORT = self.port + 11
        WS_PORT = self.port + 12

        patterns = [
            (r'^app\.contact\.dns\.socket:.*$', f'app.contact.dns.socket: 0.0.0.0:{DNS_PORT}'),
            (r'^app\.contact\.http:.*$', f'app.contact.http: http://0.0.0.0:{HTTP_PORT}'),
            (r'^app\.contact\.tunnel\.ssh\.socket:.*$', f'app.contact.tunnel.ssh.socket: 0.0.0.0:{SSH_PORT}'),
            (r'^app\.contact\.ftp\.port:.*$', f'app.contact.ftp.port: {FTP_PORT}'),
            (r'^app\.contact\.tcp:.*$', f'app.contact.tcp: 0.0.0.0:{TCP_PORT}'),
            (r'^app\.contact\.udp:.*$', f'app.contact.udp: 0.0.0.0:{UDP_PORT}'),
            (r'^app\.contact\.websocket:.*$', f'app.contact.websocket: 0.0.0.0:{WS_PORT}'),
            (r'^port:.*$', f'port: {HTTP_PORT}')
        ]

        for pattern, replacement in patterns:
            file_str = re.sub(pattern, replacement, file_str, flags=re.MULTILINE)

        
        with open(config_file, 'w') as f:
            f.write(file_str)

        return HTTP_PORT

find_port = FindPort()
caldera_server = CalderaServer()
ubuntu_client = UbuntuClient()


def run_task():
    result = find_port.get_port()

    caldera_server.preparation()

    if caldera_server.status:
        ubuntu_client.start_docker(result['HTTP_PORT'])
        return result
    else:
        return logger.error({'error': 'Failed to start Caldera'})

if __name__ == '__main__':
    run_task()
