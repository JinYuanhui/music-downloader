export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // API 路由
    if (url.pathname === '/api/download') {
      const musicUrl = url.searchParams.get('url');
      
      if (!musicUrl) {
        return new Response(JSON.stringify({ error: 'Missing url' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' }
        });
      }
      
      try {
        // 提取 chain
        const chainMatch = musicUrl.match(/chain=([A-Za-z0-9]+)/);
        if (!chainMatch) {
          return new Response(JSON.stringify({ error: 'Invalid Kugou URL' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' }
          });
        }
        
        const chain = chainMatch[1];
        const shareUrl = `https://www.kugou.com/share/${chain}.html`;
        
        // 获取分享页面
        const shareRes = await fetch(shareUrl, {
          headers: {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
          }
        });
        
        const html = await shareRes.text();
        
        // 提取 hash
        const hashMatch = html.match(/"hash":"([A-Fa-f0-9]+)"/);
        if (!hashMatch) {
          return new Response(JSON.stringify({ error: 'Cannot extract song hash' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
          });
        }
        
        const hash = hashMatch[1];
        
        // 获取歌曲信息
        const apiUrl = `https://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash=${hash}`;
        const apiRes = await fetch(apiUrl, {
          headers: {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
          }
        });
        
        const songInfo = await apiRes.json();
        
        if (songInfo.status !== 1) {
          return new Response(JSON.stringify({ error: 'Song unavailable' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
          });
        }
        
        const result = {
          success: true,
          songName: songInfo.audio_name || songInfo.songName || 'Unknown',
          artist: songInfo.author_name || 'Unknown',
          duration: songInfo.timeLength || 0,
          size: songInfo.fileSize || 0,
          downloadUrl: songInfo.url,
          hash: hash
        };
        
        return new Response(JSON.stringify(result), {
          headers: { 
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          }
        });
        
      } catch (e) {
        return new Response(JSON.stringify({ error: e.message }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }
    
    // 返回前端页面
    return new Response(HTML, {
      headers: { 'Content-Type': 'text/html;charset=UTF-8' }
    });
  }
};

const HTML = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎵 音乐下载器</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 100%;
        }
        h1 { text-align: center; color: #333; margin-bottom: 10px; font-size: 28px; }
        .subtitle { text-align: center; color: #666; margin-bottom: 30px; font-size: 14px; }
        .input-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; color: #555; font-weight: 500; }
        input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus { outline: none; border-color: #667eea; }
        .btn {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4); }
        .btn:active { transform: translateY(0); }
        .btn:disabled { background: #ccc; cursor: not-allowed; transform: none; }
        .result {
            margin-top: 20px;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }
        .result.success { background: #d4edda; color: #155724; display: block; }
        .result.error { background: #f8d7da; color: #721c24; display: block; }
        .result.loading { background: #e7f3ff; color: #004085; display: block; }
        .song-info {
            margin-top: 15px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .song-info h3 { margin-bottom: 10px; color: #333; }
        .song-info p { color: #666; margin: 5px 0; }
        .download-link {
            display: inline-block;
            margin-top: 15px;
            padding: 12px 24px;
            background: #28a745;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
        }
        .download-link:hover { background: #218838; }
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
            vertical-align: middle;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .supported {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            font-size: 13px;
        }
        .supported h4 { margin-bottom: 10px; color: #555; }
        .supported ul { list-style: none; padding-left: 0; }
        .supported li { padding: 5px 0; color: #666; }
        .supported li::before { content: "✓ "; color: #28a745; font-weight: bold; }
        .tips {
            margin-top: 15px;
            padding: 12px;
            background: #fff3cd;
            border-radius: 8px;
            font-size: 12px;
            color: #856404;
        }
        .tips strong { display: block; margin-bottom: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 音乐下载器</h1>
        <p class="subtitle">支持酷狗音乐分享链接</p>
        
        <div class="input-group">
            <label for="url">粘贴音乐链接：</label>
            <input type="text" id="url" placeholder="https://m.kugou.com/share/song.html?chain=..." autocomplete="off">
        </div>
        
        <button class="btn" id="downloadBtn" onclick="startDownload()">开始下载</button>
        
        <div class="result" id="result"></div>
        
        <div class="tips">
            <strong>💡 使用提示</strong>
            如果下载按钮无法直接下载，请长按复制链接，然后在新标签页打开即可下载。
        </div>
        
        <div class="supported">
            <h4>支持的平台</h4>
            <ul>
                <li>酷狗音乐 (kugou.com)</li>
                <li>更多平台开发中...</li>
            </ul>
        </div>
    </div>

    <script>
        function extractChain(url) {
            const patterns = [/chain=([A-Za-z0-9]+)/, /\\/share\\/([A-Za-z0-9]+)\\.html/];
            for (const pattern of patterns) {
                const match = url.match(pattern);
                if (match) return match[1];
            }
            return null;
        }
        
        function formatDuration(seconds) {
            try {
                const mins = Math.floor(seconds / 60);
                const secs = seconds % 60;
                return mins + ":" + secs.toString().padStart(2, '0');
            } catch { return '未知'; }
        }
        
        function formatSize(bytes) {
            try {
                if (bytes < 1024) return bytes + " B";
                if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
                return (bytes / (1024 * 1024)).toFixed(1) + " MB";
            } catch { return '未知'; }
        }
        
        function showError(msg) {
            const result = document.getElementById('result');
            result.className = 'result error';
            result.innerHTML = '<strong>✗ 错误</strong><br>' + msg;
        }
        
        function showSuccess(data) {
            const result = document.getElementById('result');
            result.className = 'result success';
            result.innerHTML = '<strong>✓ 解析成功！</strong>' +
                '<div class="song-info">' +
                '<h3>' + (data.songName || '未知歌曲') + '</h3>' +
                '<p>歌手：' + (data.artist || '未知') + '</p>' +
                '<p>时长：' + (data.duration || '未知') + '</p>' +
                '<p>大小：' + (data.size || '未知') + '</p>' +
                '</div>' +
                '<a href="' + data.downloadUrl + '" class="download-link" target="_blank">⬇️ 下载 MP3</a>';
        }
        
        async function startDownload() {
            const url = document.getElementById('url').value.trim();
            const btn = document.getElementById('downloadBtn');
            const result = document.getElementById('result');
            
            if (!url) { showError('请输入音乐链接'); return; }
            if (!url.includes('kugou.com')) { showError('目前仅支持酷狗音乐链接'); return; }
            
            btn.disabled = true;
            result.className = 'result loading';
            result.innerHTML = '<span class="spinner"></span>正在解析链接...';
            
            try {
                const apiUrl = '/api/download?url=' + encodeURIComponent(url);
                const res = await fetch(apiUrl);
                const data = await res.json();
                
                if (data.error) throw new Error(data.error);
                if (!data.success) throw new Error('解析失败');
                
                showSuccess({
                    songName: data.songName,
                    artist: data.artist,
                    duration: formatDuration(data.duration),
                    size: formatSize(data.size),
                    downloadUrl: data.downloadUrl
                });
            } catch (err) {
                showError(err.message || '解析失败，请稍后重试');
            } finally {
                btn.disabled = false;
            }
        }
        
        document.getElementById('url').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') startDownload();
        });
        
        window.startDownload = startDownload;
    </script>
</body>
</html>`;
