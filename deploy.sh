#!/bin/bash

# 音乐下载器一键部署脚本
# 支持: Vercel, GitHub Pages, Railway

echo "🎵 音乐下载器部署脚本"
echo "====================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查命令
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 显示菜单
show_menu() {
    echo "请选择部署方式:"
    echo ""
    echo "1) Vercel (推荐 - 最简单)"
    echo "2) GitHub Pages (免费稳定)"
    echo "3) Railway (带后端，更稳定)"
    echo "4) Docker (自有服务器)"
    echo "5) 退出"
    echo ""
}

# 部署到 Vercel
deploy_vercel() {
    echo -e "${YELLOW}正在部署到 Vercel...${NC}"
    
    if ! command_exists vercel; then
        echo "安装 Vercel CLI..."
        npm install -g vercel
    fi
    
    if [ ! -f "vercel.json" ]; then
        echo -e "${RED}错误: 未找到 vercel.json${NC}"
        return 1
    fi
    
    vercel --prod
    
    echo -e "${GREEN}✅ 部署完成!${NC}"
}

# 部署到 GitHub Pages
deploy_github_pages() {
    echo -e "${YELLOW}正在部署到 GitHub Pages...${NC}"
    
    if ! command_exists git; then
        echo -e "${RED}错误: 请先安装 Git${NC}"
        return 1
    fi
    
    # 初始化 git
    if [ ! -d ".git" ]; then
        git init
        git add .
        git commit -m "Initial commit"
    fi
    
    echo ""
    echo "请按以下步骤操作:"
    echo "1. 在 GitHub 创建新仓库 (不要初始化)"
    echo "2. 运行以下命令:"
    echo ""
    echo -e "${GREEN}   git remote add origin https://github.com/你的用户名/仓库名.git${NC}"
    echo -e "${GREEN}   git branch -M main${NC}"
    echo -e "${GREEN}   git push -u origin main${NC}"
    echo ""
    echo "3. 进入仓库 Settings → Pages"
    echo "4. Source 选择 'Deploy from a branch'"
    echo "5. Branch 选择 'main'，文件夹选择 '/ (root)'"
    echo "6. 点击 Save"
    echo ""
    echo "访问地址: https://你的用户名.github.io/仓库名/static/"
}

# 部署到 Railway
deploy_railway() {
    echo -e "${YELLOW}正在部署到 Railway...${NC}"
    
    if ! command_exists railway; then
        echo "安装 Railway CLI..."
        npm install -g @railway/cli
    fi
    
    echo ""
    echo "请按以下步骤操作:"
    echo "1. 访问 https://railway.app 并登录"
    echo "2. 创建新项目，选择从 GitHub 部署"
    echo "3. Railway 会自动识别配置并部署"
    echo ""
    echo "或者使用 CLI:"
    echo -e "${GREEN}   railway login${NC}"
    echo -e "${GREEN}   railway init${NC}"
    echo -e "${GREEN}   railway up${NC}"
}

# Docker 部署
deploy_docker() {
    echo -e "${YELLOW}正在使用 Docker 部署...${NC}"
    
    if ! command_exists docker; then
        echo -e "${RED}错误: 请先安装 Docker${NC}"
        return 1
    fi
    
    if ! command_exists docker-compose; then
        echo -e "${RED}错误: 请先安装 docker-compose${NC}"
        return 1
    fi
    
    docker-compose up -d --build
    
    echo -e "${GREEN}✅ 部署完成!${NC}"
    echo ""
    echo "访问地址: http://localhost:8765"
    echo ""
    echo "停止服务: docker-compose down"
    echo "查看日志: docker-compose logs -f"
}

# 主程序
main() {
    show_menu
    read -p "请输入选项 (1-5): " choice
    
    case $choice in
        1)
            deploy_vercel
            ;;
        2)
            deploy_github_pages
            ;;
        3)
            deploy_railway
            ;;
        4)
            deploy_docker
            ;;
        5)
            echo "再见!"
            exit 0
            ;;
        *)
            echo -e "${RED}无效选项${NC}"
            exit 1
            ;;
    esac
}

main
