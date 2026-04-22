#!/usr/bin/env python3
"""
音乐下载服务 - 支持酷狗音乐
"""
import json
import re
import os
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 8765

class MusicDownloader:
    @staticmethod
    def extract_chain_from_url(url):
        """从酷狗分享链接中提取 chain 参数"""
        patterns = [
            r'chain=([A-Za-z0-9]+)',
            r'/share/([A-Za-z0-9]+)\.html',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    @staticmethod
    def get_song_info(hash_code):
        """通过 hash 获取歌曲信息"""
        api_url = f"https://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash={hash_code}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Referer': 'https://m.kugou.com'
        }
        
        try:
            req = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                return data
        except Exception as e:
            print(f"Error getting song info: {e}")
            return None
    
    @staticmethod
    def get_song_info_by_chain(chain):
        """通过 chain 获取歌曲信息"""
        # 先访问分享页面获取 hash
        share_url = f"https://www.kugou.com/share/{chain}.html"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            req = urllib.request.Request(share_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8')
                # 提取 hash
                match = re.search(r'"hash":"([A-Fa-f0-9]+)"', html)
                if match:
                    hash_code = match.group(1)
                    return MusicDownloader.get_song_info(hash_code)
        except Exception as e:
            print(f"Error getting song by chain: {e}")
        
        return None
    
    @staticmethod
    def format_duration(seconds):
        """格式化时长"""
        try:
            seconds = int(seconds)
            minutes = seconds // 60
            secs = seconds % 60
            return f"{minutes}:{secs:02d}"
        except:
            return "未知"
    
    @staticmethod
    def format_size(bytes_size):
        """格式化文件大小"""
        try:
            bytes_size = int(bytes_size)
            if bytes_size < 1024:
                return f"{bytes_size} B"
            elif bytes_size < 1024 * 1024:
                return f"{bytes_size / 1024:.1f} KB"
            else:
                return f"{bytes_size / (1024 * 1024):.1f} MB"
        except:
            return "未知"


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/' or parsed_path.path == '/index.html':
            self.serve_file('/Users/jinyuanhui/.openclaw/workspace/music-downloader/index.html', 'text/html')
        elif parsed_path.path == '/api/download':
            self.handle_download_request()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """处理 POST 请求"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/download':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(post_data)
                url = data.get('url', '')
                self.process_download(url)
            except json.JSONDecodeError:
                self.send_json_response({'success': False, 'message': '无效的请求数据'})
        else:
            self.send_error(404)
    
    def serve_file(self, filepath, content_type):
        """提供静态文件"""
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)
    
    def send_json_response(self, data):
        """发送 JSON 响应"""
        response = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response)
    
    def process_download(self, url):
        """处理下载请求"""
        if not url:
            self.send_json_response({'success': False, 'message': '请输入链接'})
            return
        
        # 检查是否为酷狗链接
        if 'kugou.com' not in url:
            self.send_json_response({'success': False, 'message': '目前仅支持酷狗音乐链接'})
            return
        
        # 提取 chain
        chain = MusicDownloader.extract_chain_from_url(url)
        if not chain:
            self.send_json_response({'success': False, 'message': '无法解析链接，请检查链接格式'})
            return
        
        # 获取歌曲信息
        song_info = MusicDownloader.get_song_info_by_chain(chain)
        
        if not song_info:
            self.send_json_response({'success': False, 'message': '获取歌曲信息失败'})
            return
        
        if song_info.get('status') != 1:
            self.send_json_response({'success': False, 'message': '歌曲不可用或需要付费'})
            return
        
        # 提取信息
        song_name = song_info.get('songName', '未知歌曲')
        audio_name = song_info.get('audio_name', song_name)
        artist = song_info.get('author_name', '未知歌手')
        duration = MusicDownloader.format_duration(song_info.get('timeLength', 0))
        file_size = MusicDownloader.format_size(song_info.get('fileSize', 0))
        download_url = song_info.get('url', '')
        
        if not download_url:
            self.send_json_response({'success': False, 'message': '无法获取下载链接'})
            return
        
        # 返回结果
        self.send_json_response({
            'success': True,
            'songName': audio_name,
            'artist': artist,
            'duration': duration,
            'size': file_size,
            'downloadUrl': download_url
        })
    
    def handle_download_request(self):
        """处理直接下载请求（通过 query 参数）"""
        query = parse_qs(urlparse(self.path).query)
        url = query.get('url', [''])[0]
        self.process_download(url)
    
    def log_message(self, format, *args):
        """简化日志输出"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server():
    """启动服务器"""
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"🎵 音乐下载服务已启动")
    print(f"📍 访问地址: http://localhost:{PORT}")
    print(f"🛑 按 Ctrl+C 停止服务")
    print("-" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
        httpd.server_close()


if __name__ == '__main__':
    run_server()
