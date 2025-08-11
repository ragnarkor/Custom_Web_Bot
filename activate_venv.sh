#!/usr/bin/env sh
# 统一虚拟环境激活脚本
# 用法（请务必用 source 来激活到当前 shell）:
#   source ./activate_venv.sh            # 激活根目录 venv
#   source ./activate_venv.sh root       # 同上
#   source ./activate_venv.sh smart      # 激活 Smart_Play_Bot/venv

set -e
MODE="${1:-root}"

if [ "$MODE" = "smart" ]; then
  ACT_PATH="Smart_Play_Bot/venv/bin/activate"
  ENV_NAME="Smart_Play_Bot"
else
  ACT_PATH="venv/bin/activate"
  ENV_NAME="root"
fi

if [ ! -f "$ACT_PATH" ]; then
  echo "未找到虚拟环境文件: $ACT_PATH"
  printf "请先创建: python3 -m venv %s\n" "$( [ "$MODE" = "smart" ] && printf "Smart_Play_Bot/venv" || printf "venv" )"
  # 兼容被 source 和直接执行两种方式
  return 1 2>/dev/null || exit 1
fi

echo "提示: 请使用 'source ./activate_venv.sh [root|smart]' 在当前 shell 中激活。"
. "$ACT_PATH"
echo "虚拟环境($ENV_NAME)已激活: $(python -V 2>&1) -> $(which python)"
