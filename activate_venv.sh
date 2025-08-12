#!/usr/bin/env sh
# 统一虚拟环境激活脚本
# 用法（请务必用 source 来激活到当前 shell）:
#   source ./activate_venv.sh            # 激活根目录 venv
#   source ./activate_venv.sh root       # 同上
#   source ./activate_venv.sh smart      # 激活 Smart_Play_Bot/venv
#   source ./activate_venv.sh setup      # 配置虚拟环境并安装依赖

set -e

# 配置虚拟环境和安装依赖的函数
setup_env() {
  echo "开始配置虚拟环境和安装依赖..."
  
  # 检查 Python3 是否可用
  if ! command -v python3 >/dev/null 2>&1; then
    echo "错误: 未找到 python3 命令，请先安装 Python 3"
    return 1
  fi
  
  # 获取当前工作目录的绝对路径
  CURRENT_DIR=$(pwd)
  echo "当前工作目录: $CURRENT_DIR"
  
  # 创建根目录虚拟环境
  if [ ! -d "venv" ]; then
    echo "创建根目录虚拟环境..."
    python3 -m venv venv
    echo "✅ 根目录虚拟环境创建成功"
  else
    echo "✅ 根目录虚拟环境已存在"
  fi
  
  # 创建 Smart_Play_Bot 虚拟环境
  if [ ! -d "Smart_Play_Bot/venv" ]; then
    echo "创建 Smart_Play_Bot 虚拟环境..."
    cd Smart_Play_Bot
    python3 -m venv venv
    cd "$CURRENT_DIR"
    echo "✅ Smart_Play_Bot 虚拟环境创建成功"
  else
    echo "✅ Smart_Play_Bot 虚拟环境已存在"
  fi
  
  # 激活根目录虚拟环境并安装依赖
  echo "安装根目录依赖..."
  if [ -f "venv/bin/activate" ]; then
    . venv/bin/activate
    echo "升级 pip..."
    python -m pip install --upgrade pip
    if [ -f "requirements.txt" ]; then
      echo "安装根目录 requirements.txt 中的依赖..."
      python -m pip install -r requirements.txt
      echo "✅ 根目录依赖安装完成"
    else
      echo "⚠️  根目录没有找到 requirements.txt 文件"
    fi
    deactivate
  else
    echo "❌ 根目录虚拟环境激活失败"
  fi
  
  # 激活 Smart_Play_Bot 虚拟环境并安装依赖
  echo "安装 Smart_Play_Bot 依赖..."
  if [ -f "Smart_Play_Bot/venv/bin/activate" ]; then
    . Smart_Play_Bot/venv/bin/activate
    echo "升级 pip..."
    python -m pip install --upgrade pip
    if [ -f "Smart_Play_Bot/requirements.txt" ]; then
      echo "安装 Smart_Play_Bot requirements.txt 中的依赖..."
      python -m pip install -r Smart_Play_Bot/requirements.txt
      echo "✅ Smart_Play_Bot 依赖安装完成"
    else
      echo "⚠️  Smart_Play_Bot 没有找到 requirements.txt 文件"
    fi
    
    # 安装兼容性包
    echo "安装兼容性包..."
    python -m pip install urllib3==1.26.18
    python -m pip install PyYAML==6.0.1
    echo "✅ 兼容性包安装完成"
    
    # 验证安装
    echo "验证安装..."
    python -c "import yaml; print('✓ PyYAML 安装成功')" 2>/dev/null || echo "✗ PyYAML 安装失败"
    python -c "import selenium; print('✓ Selenium 安装成功')" 2>/dev/null || echo "✗ Selenium 安装失败"
    python -c "import pandas; print('✓ Pandas 安装成功')" 2>/dev/null || echo "✗ Pandas 安装失败"
    python -c "import numpy; print('✓ NumPy 安装成功')" 2>/dev/null || echo "✗ NumPy 安装失败"
    
    deactivate
  else
    echo "❌ Smart_Play_Bot 虚拟环境激活失败"
  fi
  
  echo "虚拟环境配置和依赖安装完成！"
  echo "现在可以使用以下命令激活虚拟环境："
  echo "  source ./activate_venv.sh root    # 激活根目录虚拟环境"
  echo "  source ./activate_venv.sh smart   # 激活 Smart_Play_Bot 虚拟环境"
}

MODE="${1:-root}"

# 如果是 setup 模式，执行配置
if [ "$MODE" = "setup" ]; then
  setup_env
  return 0
fi

if [ "$MODE" = "smart" ]; then
  ACT_PATH="Smart_Play_Bot/venv/bin/activate"
  ENV_NAME="Smart_Play_Bot"
else
  ACT_PATH="venv/bin/activate"
  ENV_NAME="root"
fi

if [ ! -f "$ACT_PATH" ]; then
  echo "未找到虚拟环境文件: $ACT_PATH"
  echo "请先运行配置命令: source ./activate_venv.sh setup"
  printf "或者手动创建: python3 -m venv %s\n" "$( [ "$MODE" = "smart" ] && printf "Smart_Play_Bot/venv" || printf "venv" )"
  # 兼容被 source 和直接执行两种方式
  return 1 2>/dev/null || exit 1
fi

echo "提示: 请使用 'source ./activate_venv.sh [root|smart]' 在当前 shell 中激活。"
. "$ACT_PATH"

# 尝试获取Python版本信息，使用多种可能的命令
PYTHON_VERSION=""
PYTHON_PATH=""

if command -v python >/dev/null 2>&1; then
  PYTHON_VERSION=$(python -V 2>&1)
  PYTHON_PATH=$(which python)
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_VERSION=$(python3 -V 2>&1)
  PYTHON_PATH=$(which python3)
else
  PYTHON_VERSION="Python not found"
  PYTHON_PATH="Not available"
fi

echo "虚拟环境($ENV_NAME)已激活: $PYTHON_VERSION -> $PYTHON_PATH"
