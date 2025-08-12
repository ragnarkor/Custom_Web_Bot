# Smart Play Bot Scheduler

自动定时执行 Smart Play Bot 的调度器脚本。

## 功能特性

- **定时执行**：在每天 11:20 AM - 11:40 AM 之间自动执行
- **进程监控**：实时监控 bot 进程状态
- **异常处理**：自动处理异常终止和重启
- **超时控制**：超过 15 分钟自动终止并重启
- **浏览器清理**：自动清理残留的浏览器进程
- **日志记录**：详细记录所有操作和错误信息
- **成功退出**：完成支付后自动结束任务

## 文件说明

- `scheduler.py` - 主调度器脚本
- `requirements.txt` - 依赖包列表
- `start.sh` - Linux/macOS 启动脚本
- `start.bat` - Windows 启动脚本
- `scheduler.log` - 运行日志文件

## 使用方法

### Linux/macOS
```bash
chmod +x start.sh
./start.sh
```

### Windows
```cmd
start.bat
```

### 手动运行
```bash
# 激活虚拟环境
source ../Smart_Play_Bot/venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行调度器
python scheduler.py
```

## 工作流程

1. **等待时间**：在 11:20 AM 之前等待
2. **执行时间**：11:20 AM - 11:40 AM 之间执行 bot
3. **监控状态**：实时监控 bot 运行状态
4. **异常处理**：遇到错误自动重启
5. **超时控制**：超过 15 分钟自动重启
6. **成功完成**：完成支付后退出调度器

## 日志说明

- `scheduler.log` 文件记录所有操作日志
- 控制台实时显示运行状态
- 包含时间戳、日志级别和详细信息

## 注意事项

- 确保 `../Smart_Play_Bot/smart_play_bot.py` 文件存在
- 确保 `../Smart_Play_Bot/venv` 虚拟环境配置正确
- 调度器会在 11:40 AM 后自动退出
- 可以通过 Ctrl+C 手动停止调度器

## 依赖要求

- Python 3.6+
- psutil 5.8.0+
- 其他依赖见 `requirements.txt`
