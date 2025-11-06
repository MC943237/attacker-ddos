#!/bin/bash

cd "$(dirname "$0")"

# 检查依赖
if ! command -v python3 &> /dev/null; then
    echo "错误：未安装Python3，请先执行 sudo apt install python3"
    exit 1
fi
if ! command -v php &> /dev/null; then
    echo "错误：未安装PHP，请先执行 sudo apt install php"
    exit 1
fi

# 检查所有文件是否存在
required_files=("网页.html" "api.php" "get_log.php" "visitor.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "错误：缺失文件 $file，请确保所有文件在同一目录"
        exit 1
    fi
done

# 安装Python依赖
echo "正在安装Python依赖..."
pip3 install requests --upgrade &> /dev/null

# 启动PHP服务器（根目录为当前目录）
echo "启动PHP服务器..."
php -S localhost:8000 -t . &
SERVER_PID=$!

# 等待服务器启动
sleep 2

# 修复：不依赖默认浏览器，直接提示手动访问
echo "✅ 系统已启动！"
echo "请手动打开浏览器，访问以下地址："
echo "http://localhost:8000/网页.html"
echo "----------------------------------------"
echo "按 Ctrl+C 可停止所有服务"

wait $SERVER_PID