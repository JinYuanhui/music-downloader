# 🚀 部署指南

## 方案对比

| 方案 | 难度 | 费用 | 速度 | 推荐度 |
|------|------|------|------|--------|
| **GitHub Pages** | ⭐ 最简单 | 免费 | 快 | ⭐⭐⭐⭐⭐ |
| **Vercel** | ⭐ 简单 | 免费 | 很快 | ⭐⭐⭐⭐⭐ |
| **Netlify** | ⭐ 简单 | 免费 | 快 | ⭐⭐⭐⭐ |
| **Railway** | ⭐⭐ 中等 | 免费额度 | 快 | ⭐⭐⭐⭐ |
| **自有服务器** | ⭐⭐⭐ 较难 | 付费 | 取决于服务器 | ⭐⭐⭐ |

---

## 方案一：GitHub Pages（推荐 ⭐⭐⭐⭐⭐）

最简单，完全免费，全球 CDN 加速。

### 步骤：

1. **创建 GitHub 仓库**
   ```bash
   cd /Users/jinyuanhui/.openclaw/workspace/music-downloader
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **在 GitHub 上创建新仓库**，然后：
   ```bash
   git remote add origin https://github.com/你的用户名/music-downloader.git
   git branch -M main
   git push -u origin main
   ```

3. **开启 GitHub Pages**
   - 进入仓库 → Settings → Pages
   - Source 选择 "Deploy from a branch"
   - Branch 选择 "main"，文件夹选择 "/ (root)"
   - 点击 Save

4. **访问你的站点**
   ```
   https://你的用户名.github.io/music-downloader/static/
   ```

✅ **完成！** 手机/电脑都能访问

---

## 方案二：Vercel（推荐 ⭐⭐⭐⭐⭐）

最快的部署方式，自动 HTTPS，全球 CDN。

### 步骤：

1. **安装 Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **部署**
   ```bash
   cd /Users/jinyuanhui/.openclaw/workspace/music-downloader/static
   vercel --prod
   ```

3. **按提示操作**，完成后会给你一个链接：
   ```
   https://music-downloader-xxx.vercel.app
   ```

✅ **完成！**

---

## 方案三：Railway（带后端）

如果需要后端支持（比如绕过 CORS 限制），部署完整版。

### 步骤：

1. **Fork 到 GitHub**（同上）

2. **在 Railway 部署**
   - 访问 https://railway.app
   - 用 GitHub 登录
   - New Project → Deploy from GitHub repo
   - 选择仓库
   - Railway 自动识别 `requirements.txt` 和 `Procfile`

3. **获取域名**
   - 部署完成后，Settings → Domains
   - 会给你一个 `.up.railway.app` 域名

✅ **完成！**

---

## 方案四：自有服务器/VPS

### 使用 Docker 部署：

```bash
# 构建镜像
docker build -t music-downloader .

# 运行
docker run -d -p 8765:8765 --name music-downloader music-downloader
```

### 或使用 docker-compose：

```yaml
version: '3'
services:
  music-downloader:
    build: .
    ports:
      - "8765:8765"
    restart: unless-stopped
```

---

## 📱 手机添加到桌面

部署完成后，像 APP 一样使用：

**iOS Safari：**
1. 打开网站
2. 点击底部分享按钮
3. 选择「添加到主屏幕」

**Android Chrome：**
1. 打开网站
2. 点击菜单（三个点）
3. 选择「添加到主屏幕」

---

## 🔧 自定义域名（可选）

所有平台都支持绑定自己的域名：

1. 在平台设置中添加自定义域名
2. 在你的 DNS 服务商添加 CNAME 记录
3. 等待 DNS 生效

---

## ⚠️ 注意事项

1. **GitHub Pages / Vercel 纯前端版本**：
   - 依赖第三方 CORS 代理（allorigins.win）
   - 如果代理服务不稳定，可能偶尔失败
   - 免费、无需维护

2. **Railway 后端版本**：
   - 更稳定，不依赖第三方代理
   - 每月有免费额度限制
   - 需要维护后端服务

3. **版权问题**：
   - 仅下载自己有权限的歌曲
   - 不要用于商业用途

---

## 🆘 遇到问题？

1. **纯前端版本解析失败**：
   - 可能是 CORS 代理限流，稍后重试
   - 尝试使用后端版本

2. **部署失败**：
   - 检查文件路径是否正确
   - 查看平台日志

3. **下载失败**：
   - 酷狗 API 可能变化
   - VIP 歌曲无法下载

---

## 📁 文件说明

```
music-downloader/
├── static/                 # 纯前端版本（GitHub Pages/Vercel）
│   └── index.html         # 单文件，可直接部署
├── app.py                 # Flask 后端（Railway/Render）
├── server.py              # 纯 Python 后端（本地测试）
├── requirements.txt       # Python 依赖
├── Procfile              # Railway/Heroku 配置
├── Dockerfile            # Docker 部署
├── DEPLOY.md             # 本文件
└── .github/
    └── workflows/
        └── deploy.yml    # GitHub Actions 自动部署
```

---

**推荐新手使用 GitHub Pages 或 Vercel，最简单！**
