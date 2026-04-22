from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/download')
def download():
    url = request.args.get('url', '')
    
    if not url:
        return jsonify({'error': 'Missing url'}), 400
    
    try:
        # 提取 chain
        chain_match = re.search(r'chain=([A-Za-z0-9]+)', url)
        if not chain_match:
            return jsonify({'error': 'Invalid Kugou URL'}), 400
        
        chain = chain_match.group(1)
        share_url = f'https://www.kugou.com/share/{chain}.html'
        
        # 获取分享页面
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        }
        res = requests.get(share_url, headers=headers, timeout=10)
        html = res.text
        
        # 提取 hash
        hash_match = re.search(r'"hash":"([A-Fa-f0-9]+)"', html)
        if not hash_match:
            return jsonify({'error': 'Cannot extract song hash'}), 500
        
        hash_val = hash_match.group(1)
        
        # 获取歌曲信息
        api_url = f'https://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash={hash_val}'
        api_res = requests.get(api_url, headers=headers, timeout=10)
        song_info = api_res.json()
        
        if song_info.get('status') != 1:
            return jsonify({'error': 'Song unavailable or requires payment'}), 500
        
        result = {
            'success': True,
            'songName': song_info.get('audio_name') or song_info.get('songName', 'Unknown'),
            'artist': song_info.get('author_name', 'Unknown'),
            'duration': song_info.get('timeLength', 0),
            'size': song_info.get('fileSize', 0),
            'downloadUrl': song_info.get('url'),
            'hash': hash_val
        }
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8765))
    app.run(host='0.0.0.0', port=port)
