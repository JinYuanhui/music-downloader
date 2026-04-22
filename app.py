"""
音乐下载服务 - Flask版本（适合部署到云端）
支持平台: Railway, Render, Heroku等
"""
import json
import re
import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 配置
PORT = int(os.environ.get('PORT', 8765))


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
            response = requests.get(api_url, headers=headers, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error getting song info: {e}")
            return None
    
    @staticmethod
    def get_song_info_by_chain(chain):
        """通过 chain 获取歌曲信息"""
        share_url = f"https://www.kugou.com/share/{chain}.html"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            response = requests.get(share_url, headers=headers, timeout=10)
            html = response.text
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


@app.route('/')
def index():
    """主页"""
    return send_from_directory('.', 'index.html')


@app.route('/api/download', methods=['POST', 'GET'])
def download():
    """处理下载请求"""
    if request.method == 'POST':
        data = request.get_json()
        url = data.get('url', '') if data else ''
    else:
        url = request.args.get('url', '')
    
    if not url:
        return jsonify({'success': False, 'message': '请输入链接'})
    
    # 检查是否为酷狗链接
    if 'kugou.com' not in url:
        return jsonify({'success': False, 'message': '目前仅支持酷狗音乐链接'})
    
    # 提取 chain
    chain = MusicDownloader.extract_chain_from_url(url)
    if not chain:
        return jsonify({'success': False, 'message': '无法解析链接，请检查链接格式'})
    
    # 获取歌曲信息
    song_info = MusicDownloader.get_song_info_by_chain(chain)
    
    if not song_info:
        return jsonify({'success': False, 'message': '获取歌曲信息失败'})
    
    if song_info.get('status') != 1:
        return jsonify({'success': False, 'message': '歌曲不可用或需要付费'})
    
    # 提取信息
    song_name = song_info.get('songName', '未知歌曲')
    audio_name = song_info.get('audio_name', song_name)
    artist = song_info.get('author_name', '未知歌手')
    duration = MusicDownloader.format_duration(song_info.get('timeLength', 0))
    file_size = MusicDownloader.format_size(song_info.get('fileSize', 0))
    download_url = song_info.get('url', '')
    
    if not download_url:
        return jsonify({'success': False, 'message': '无法获取下载链接'})
    
    return jsonify({
        'success': True,
        'songName': audio_name,
        'artist': artist,
        'duration': duration,
        'size': file_size,
        'downloadUrl': download_url
    })


@app.route('/api/health')
def health():
    """健康检查"""
    return jsonify({'status': 'ok', 'service': 'music-downloader'})


if __name__ == '__main__':
    print(f"🎵 音乐下载服务已启动")
    print(f"📍 访问地址: http://localhost:{PORT}")
    print(f"🛑 按 Ctrl+C 停止服务")
    app.run(host='0.0.0.0', port=PORT, debug=False)
