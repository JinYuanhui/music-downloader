# 🎵 音乐下载器

一个简单的音乐下载工具，支持从酷狗音乐分享链接下载 MP3 文件。

## ✨ 功能

- ✅ 支持酷狗音乐分享链接解析
- ✅ 自动获取歌曲信息（歌名、歌手、时长、大小）
- ✅ 一键下载 MP3 文件
- ✅ 响应式设计，支持手机/电脑

## 🚀 快速开始

### 方式一：本地运行（最简单）

```bash
cd music-downloader
./start.sh
```

访问 http://localhost:8765

### 方式二：部署到线上

查看 [DEPLOY.md](DEPLOY.md) 了解各种部署方案。

**推荐方案：**
1. **Vercel** - 一键部署，全球 CDN
2. **GitHub Pages** - 完全免费，稳定可靠
3. **Railway** - 带后端，更稳定

## 📱 使用说明

1. 在酷狗音乐 APP 中找到想下载的歌曲
2. 点击「分享」→「复制链接」
3. 将链接粘贴到网页输入框
4. 点击「开始下载」
5. 解析成功后，点击下载按钮即可

## 📁 文件结构

```
music-downloader/
├── static/                 # 纯前端版本
│   └── index.html         # 可直接部署到 GitHub Pages/Vercel
├── app.py                 # Flask 后端版本
├── server.py              # 本地测试版本
├── requirements.txt       # Python 依赖
├── deploy.sh              # 一键部署脚本
├── Dockerfile             # Docker 部署
└── DEPLOY.md              # 详细部署文档
```

## 🛠️ 技术栈

- **前端**: HTML + CSS + JavaScript (原生)
- **后端**: Python + Flask
- **部署**: Vercel / GitHub Pages / Railway / Docker

## ⚠️ 注意事项

1. 仅支持免费歌曲（非 VIP 专属）
2. 下载的音质通常为 128kbps
3. 请遵守版权法规，仅下载自己有权限的歌曲

## 📄 许可

MIT License
