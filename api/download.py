from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse
import re

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # 解析 query 参数
        path = self.path
        if '?' not in path:
            self.wfile.write(json.dumps({'error': 'Missing url parameter'}).encode())
            return
            
        query = urllib.parse.parse_qs(path.split('?')[1])
        url = query.get('url', [''])[0]
        
        if not url:
            self.wfile.write(json.dumps({'error': 'Empty url'}).encode())
            return
        
        try:
            # 提取 chain
            chain_match = re.search(r'chain=([A-Za-z0-9]+)', url)
            if not chain_match:
                self.wfile.write(json.dumps({'error': 'Invalid Kugou URL'}).encode())
                return
            
            chain = chain_match.group(1)
            share_url = f'https://www.kugou.com/share/{chain}.html'
            
            # 获取分享页面
            req = urllib.request.Request(share_url, headers={
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
            })
            with urllib.request.urlopen(req, timeout=10) as res:
                html = res.read().decode('utf-8')
            
            # 提取 hash
            hash_match = re.search(r'"hash":"([A-Fa-f0-9]+)"', html)
            if not hash_match:
                self.wfile.write(json.dumps({'error': 'Cannot extract song hash'}).encode())
                return
            
            hash_val = hash_match.group(1)
            
            # 获取歌曲信息
            api_url = f'https://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash={hash_val}'
            req2 = urllib.request.Request(api_url, headers={
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
            })
            with urllib.request.urlopen(req2, timeout=10) as res2:
                song_info = json.loads(res2.read().decode('utf-8'))
            
            if song_info.get('status') != 1:
                self.wfile.write(json.dumps({'error': 'Song unavailable or requires payment'}).encode())
                return
            
            result = {
                'success': True,
                'songName': song_info.get('audio_name') or song_info.get('songName', 'Unknown'),
                'artist': song_info.get('author_name', 'Unknown'),
                'duration': song_info.get('timeLength', 0),
                'size': song_info.get('fileSize', 0),
                'downloadUrl': song_info.get('url'),
                'hash': hash_val
            }
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
