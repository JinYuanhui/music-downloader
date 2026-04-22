#!/bin/bash

# 初始化 Git 仓库并推送到 GitHub

echo "🎵 初始化 Git 仓库"
echo "=================="
echo ""

# 检查 git
if ! command -v git &> /dev/null; then
    echo "❌ 请先安装 Git"
    exit 1
fi

# 初始化
git init

# 添加文件
git add .

# 提交
git commit -m "Initial commit: 音乐下载器"

echo ""
echo "✅ Git 仓库已初始化"
echo ""
echo "下一步:"
echo "1. 在 GitHub 创建新仓库 (https://github.com/new)"
echo "2. 不要勾选 'Initialize this repository with a README'"
echo "3. 复制仓库地址"
echo "4. 运行以下命令:"
echo ""
echo "   git remote add origin https://github.com/你的用户名/仓库名.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
