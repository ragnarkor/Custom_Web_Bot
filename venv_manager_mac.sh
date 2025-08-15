#!/usr/bin/env sh
# 统一虚拟环境激活脚本
# 用法（请务必用 source 来激活到当前 shell）：
#   source ./activate_venv.sh            # 激活根目录 venv
#   source ./activate_venv.sh root       # 同上
#   source ./activate_venv.sh smart      # 激活 Smart_Play_Bot/venv
#   source ./activate_venv.sh setup      # 配置虚拟环境并安装依赖

set -e

# 自动检测 python/python3
find_python() {
  if command -v python >/dev/null 2>&1; then
    echo python
  elif command -v python3 >/dev/null 2>&1; then
    echo python3
  else
    echo "未找到 python 或 python3，请先安装 Python 3" >&2
    return 127
  fi
}

# 补软链接，确保 venv/bin/python 存在
ensure_python_symlink() {
  VENV_PATH="$1"
  if [ -d "$VENV_PATH" ]; then
    if [ ! -f "$VENV_PATH/bin/python" ] && [ -f "$VENV_PATH/bin/python3" ]; then
      ln -sf "$VENV_PATH/bin/python3" "$VENV_PATH/bin/python"
    fi
  fi
}

# 配置虚拟环境和安装依赖的函数
setup_env() {
  echo "[INFO] 配置虚拟环境和依赖..."

  # 检查 Python3 是否可用
  PY=$(find_python)
  if [ "$?" -ne 0 ]; then
    return 1 2>/dev/null || exit 1
  fi

  CURRENT_DIR=$(pwd)

  # 创建根目录虚拟环境
  if [ ! -d "venv" ]; then
    echo "[INFO] 创建根目录虚拟环境..."
    $PY -m venv venv
  fi
  ensure_python_symlink "venv"

  # 创建 Smart_Play_Bot 虚拟环境
  if [ ! -d "Smart_Play_Bot/venv" ]; then
    echo "[INFO] 创建 Smart_Play_Bot 虚拟环境..."
    cd Smart_Play_Bot
    $PY -m venv venv
    cd "$CURRENT_DIR"
  fi
  ensure_python_symlink "Smart_Play_Bot/venv"

  # 创建 Scheduler_Bot 虚拟环境
  if [ ! -d "Scheduler_Bot/venv" ]; then
    echo "[INFO] 创建 Scheduler_Bot 虚拟环境..."
    cd Scheduler_Bot
    $PY -m venv venv
    cd "$CURRENT_DIR"
  fi
  ensure_python_symlink "Scheduler_Bot/venv"

  # 安装根目录依赖
  if [ -f "venv/bin/activate" ]; then
    . venv/bin/activate
    ensure_python_symlink "$VIRTUAL_ENV"
    PY=$(find_python)
    $PY -m pip install --upgrade pip > /dev/null
    if [ -f "requirements.txt" ]; then
      $PY -m pip install -r requirements.txt
    fi
    deactivate
  fi

  # 安装 Smart_Play_Bot 依赖
  if [ -f "Smart_Play_Bot/venv/bin/activate" ]; then
    . Smart_Play_Bot/venv/bin/activate
    ensure_python_symlink "$VIRTUAL_ENV"
    PY=$(find_python)
    $PY -m pip install --upgrade pip > /dev/null
    if [ -f "Smart_Play_Bot/requirements.txt" ]; then
      $PY -m pip install -r Smart_Play_Bot/requirements.txt
    fi
    $PY -m pip install urllib3==1.26.18 PyYAML==6.0.1 > /dev/null
    deactivate
  fi

  # 安装 Scheduler_Bot 依赖
  if [ -f "Scheduler_Bot/venv/bin/activate" ]; then
    . Scheduler_Bot/venv/bin/activate
    ensure_python_symlink "$VIRTUAL_ENV"
    PY=$(find_python)
    $PY -m pip install --upgrade pip > /dev/null
    if [ -f "Scheduler_Bot/requirements.txt" ]; then
      $PY -m pip install -r Scheduler_Bot/requirements.txt
    fi
    deactivate
  fi

  echo "[INFO] 虚拟环境和依赖配置完成"
}

MODE="${1:-root}"

# 如果是 setup 模式，执行配置
if [ "$MODE" = "setup" ]; then
  setup_env
  return 0
fi

if [ "$MODE" = "scheduler" ]; then
  ACT_PATH="Scheduler_Bot/venv/bin/activate"
  ENV_NAME="Scheduler_Bot"
elif [ "$MODE" = "smart" ]; then
  ACT_PATH="Smart_Play_Bot/venv/bin/activate"
  ENV_NAME="Smart_Play_Bot"
else
  ACT_PATH="venv/bin/activate"
  ENV_NAME="root"
fi

if [ "$MODE" = "all" ]; then
  echo "[ALL] 开始一键配置所有虚拟环境和依赖..."
  (
    source "$0" setup
  )
  echo "[ALL] 所有虚拟环境和依赖已配置完成！"
  echo "可用以下命令分别激活："
  echo "  source ./activate_venv.sh root"
  echo "  source ./activate_venv.sh smart"
  echo "  source ./activate_venv.sh scheduler"
  return 0
fi

if [ ! -f "$ACT_PATH" ]; then
  echo "未找到虚拟环境文件: $ACT_PATH"
  echo "请先运行配置命令: source ./activate_venv.sh setup"
  printf "或者手动创建: %s -m venv %s\n" "$(find_python)" "$( [ "$MODE" = "smart" ] && printf "Smart_Play_Bot/venv" || printf "venv" )"
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

# 脚本结尾，防止终端自动关闭
if [ "$PS1" ]; then
  echo "按回车键退出..."; read
fi
