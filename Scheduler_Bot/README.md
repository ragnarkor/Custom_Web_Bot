# Smart Play Bot Scheduler

智能预订机器人调度器，在指定时间窗口内执行 Smart Play Bot，具有完整的进程监控和异常处理。

## ✨ 主要特性

### 🕐 智能时间窗口管理
- **执行窗口**: 每天 00:00 - 09:00（可配置）
- **智能重试**: 窗口内持续重试直到成功
- **初次执行**: 如果错过窗口，等待下一个窗口开始
- **完成后**: 窗口结束时自动停止

### 🔄 进程监控与异常处理
- **超时控制**: 单次运行超过 15 分钟自动重启
- **进程清理**: 自动清理浏览器和机器人进程
- **异常重试**: 失败后自动重试，无重试次数限制
- **成功检测**: 检测到支付完成后自动结束

### 📋 日志与监控
- **实时日志**: 同时输出到文件和控制台
- **状态标记**: 清晰的状态提示（START, SUCCESS, FAILED 等）
- **编码优化**: 解决 Windows 控制台中文显示问题

## 🚀 快速开始

### Windows 用户

#### 方法 1: 使用启动脚本（推荐）
```cmd
# 双击运行或在命令行执行
start.bat
```

启动脚本会：
1. 检查并激活虚拟环境
2. 自动安装/更新依赖
3. 可选择调整预订时间
4. 启动调度器

#### 方法 2: 手动运行
```cmd
# 激活虚拟环境
cd ..\Smart_Play_Bot\venv\Scripts
.\Activate.ps1
cd ..\..\..\Scheduler_Bot

# 安装依赖
pip install -r requirements.txt

# 运行调度器
python scheduler.py
```

### macOS/Linux 用户

#### 方法 1: 使用启动脚本（推荐）
```bash
# 给予执行权限（首次使用）
chmod +x start.sh

# 运行启动脚本
./start.sh
```

启动脚本会：
1. 检查虚拟环境是否存在
2. 激活 Smart_Play_Bot 的虚拟环境
3. 安装/更新依赖
4. 启动调度器

#### 方法 2: 手动运行
```bash
# 激活虚拟环境
cd ../Smart_Play_Bot
source venv/bin/activate
cd ../Scheduler_Bot

# 安装依赖
pip install -r requirements.txt

# 运行调度器
python scheduler.py
```

## ⚙️ 配置说明

### 时间窗口配置
编辑 `scheduler.py` 文件中的时间设置：

```python
# 修改执行时间窗口
self.window_start_time = dt_time(0, 0)   # 开始时间 00:00
self.window_end_time = dt_time(9, 0)     # 结束时间 09:00
```

### 超时时间配置
```python
# 修改单次运行超时时间（分钟）
self.max_runtime = 15 * 60  # 15 分钟
```

## 📁 项目结构

```
Scheduler_Bot/
├── scheduler.py          # 主调度器脚本
├── requirements.txt      # Python 依赖包
├── start.sh             # macOS/Linux 启动脚本
├── start.bat            # Windows 启动脚本
├── scheduler.log        # 运行日志文件
└── README.md            # 本说明文档
```

## 🔧 环境准备

### 前置要求
1. **Python 3.8+** 已安装
2. **Smart_Play_Bot** 目录存在且已配置
3. **Smart_Play_Bot 虚拟环境** 已创建且包含必要依赖

### 依赖包说明
- `psutil>=5.8.0` - 进程管理
- `PyYAML>=6.0` - 配置文件解析

## 📊 运行状态说明

### 日志状态标记
- `[START]` - 调度器启动
- `[SUCCESS]` - 机器人执行成功
- `[FAILED]` - 机器人执行失败
- `[TIMEOUT]` - 执行超时
- `[RETRY]` - 重试执行
- `[STOP]` - 用户手动停止
- `[END]` - 调度器结束

### 典型运行流程
```
[START] Smart Play Bot Scheduler started
Execution window active (00:00 - 09:00)
Bot started (PID: 12345)
[BOT] Loading to login page
[BOT] Logged in
[BOT] Starting payment process...
[SUCCESS] Bot completed successfully with payment
[SUCCESS] Scheduler completed successfully!
[END] Scheduler finished
```

## 📝 日志管理

### 查看实时日志
```bash
# Windows PowerShell
Get-Content scheduler.log -Wait -Tail 50

# macOS/Linux
tail -f scheduler.log
```

### 查看历史日志
```bash
# 查看最后 100 行
tail -n 100 scheduler.log

# 搜索特定状态
grep "SUCCESS" scheduler.log
grep "FAILED" scheduler.log
```

## 🛠️ 故障排除

### 常见问题

#### 1. 找不到虚拟环境
```
[ERROR] Virtual environment not found
```
**解决方法**: 确保 `../Smart_Play_Bot/venv` 目录存在并已正确配置

#### 2. 找不到机器人脚本
```
[ERROR] smart_play_bot.py not found
```
**解决方法**: 确保 `../Smart_Play_Bot/smart_play_bot.py` 文件存在

#### 3. 编码错误（Windows）
```
UnicodeEncodeError: 'charmap' codec can't encode
```
**解决方法**: 已在代码中修复，使用 UTF-8 编码处理

#### 4. 权限问题（macOS/Linux）
```
Permission denied: ./start.sh
```
**解决方法**: 
```bash
chmod +x start.sh
```

### 手动停止调度器
- **Windows**: `Ctrl + C`
- **macOS/Linux**: `Ctrl + C`

## 🔄 更新日志

### v2.0 (最新)
- ✅ 移除重试次数限制，在执行窗口内持续重试
- ✅ 优化日志输出，使用状态标记替代 emoji
- ✅ 修复 Windows 控制台编码问题
- ✅ 简化代码结构，提高可维护性
- ✅ 改进跨平台兼容性

### v1.0
- ✅ 基础调度功能
- ✅ 时间窗口管理
- ✅ 进程监控和清理
- ✅ 异常处理和重试

## 📞 技术支持

如遇到问题，请检查：
1. **日志文件** `scheduler.log` 中的错误信息
2. **虚拟环境** 是否正确激活
3. **依赖包** 是否完整安装
4. **文件路径** 是否正确

---

**注意**: 本调度器设计为在执行窗口内持续运行，请确保在合适的时间启动，避免长时间等待。