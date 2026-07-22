import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/render', methods=['POST'])
def render(): 
    data = request.get_json()
    script = data.get('script', 'Alpha Tech Kingdom')
    safe_script = script.replace('"', '\\"')
    cmd = f'blender --background --python "blender_viral.py" -- "{safe_script}"'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        return jsonify({"status": "ok", "output": result.stdout})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
