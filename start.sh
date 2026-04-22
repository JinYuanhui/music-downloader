#!/bin/bash

echo "🎵 启动音乐下载服务..."
cd "$(dirname "$0")"
python3 server.py
