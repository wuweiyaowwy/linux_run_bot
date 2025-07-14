#!/bin/bash

# 设置虚拟环境的目录
VENV_DIR="venv"

# 尝试激活虚拟环境
activate_venv() {
    if [ -f "$VENV_DIR/bin/activate" ]; then
        echo "虚拟环境已找到，正在激活..."
        source "$VENV_DIR/bin/activate"
    else
        echo "虚拟环境未找到。"
        return 1
    fi
}

# 运行 Python 脚本
run_python_script() {
    echo "正在运行 Python 脚本..."
    python bot.py  # 替换为你想要运行的 Python 脚本
}

# 尝试执行脚本
activate_venv
if ! run_python_script; then
    echo "运行失败，正在创建虚拟环境..."

    # 如果运行失败，则创建新的虚拟环境
    python3 -m venv "$VENV_DIR"
    
    # 激活新创建的虚拟环境
    source "$VENV_DIR/bin/activate"
    
    # 安装依赖（如果有 requirements.txt 文件）
    if [ -f "requirements.txt" ]; then
        echo "正在安装依赖..."
        pip install -r requirements.txt
    else
        echo "未找到 requirements.txt 文件，跳过依赖安装。"
    fi
    
    # 再次尝试运行脚本
    run_python_script
fi
