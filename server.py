from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os
import shutil

app = Flask(__name__)
CORS(app)

@app.route('/get_url', methods=['GET'])
def get_url():
    output = subprocess.check_output(['python3', 'app.py']).decode('utf-8')
    print(output)
    #return output
    return jsonify({'url': f'http://localhost:{output}'})
    #return jsonify({'infol': f'{output}'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
