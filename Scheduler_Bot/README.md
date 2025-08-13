# Smart Play Bot Scheduler

智能预订机器人调度器，在指定时间窗口内执行Smart Play Bot，具有完整的进程监控和异常处理。

## 新功能特性

### 1. 执行时间调整
- 执行时间从原来的11:20-11:40改为**凌晨0点到早上9点之间**
- 保持原有的主要执行逻辑不变
- 在时间窗口内持续尝试，直到预订成功

### 2. 自动日期更新
- 自动将`Smart_Play_Bot/config.yml`中的`booking_month`和`booking_day`设置为当天日期+6天
- 无需手动修改配置文件
- 确保始终预订正确的日期

### 3. 完整的进程监控
- **异常终止处理**: 遇到异常终止时记录日志，清理浏览器进程，重新执行
- **超时控制**: 每运行超过15分钟自动终止并重新执行
- **成功检测**: 只有成功执行完`bot.payment()`才结束整个定时任务
- **浏览器清理**: 自动清理残留的浏览器进程

## 使用方法

### 启动Scheduler
```bash
# Linux/macOS
./start.sh

# Windows
start.bat

# 或者直接运行Python脚本
python scheduler.py
```

### 手动更新日期配置
```bash
python -c "
import yaml
from datetime import datetime, timedelta
from pathlib import Path

# 计算目标日期
today = datetime.now()
target_date = today + timedelta(days=6)
target_month = str(target_date.month)
target_day = str(target_date.day)

print(f'当前日期: {today.strftime(\"%Y-%m-%d\")}')
print(f'目标日期 (+6天): {target_date.strftime(\"%Y-%m-%d\")}')
print(f'月份: {target_month}, 日期: {target_day}')

# 更新配置文件
config_file = Path('../Smart_Play_Bot/config.yml')
if config_file.exists():
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    config['booking_month'] = target_month
    config['booking_day'] = target_day
    
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print('配置文件更新成功！')
else:
    print('找不到配置文件')
"
```

## 配置说明

### 执行时间窗口
- **开始时间**: 凌晨 00:00
- **结束时间**: 早上 09:00
- **执行模式**: 在时间窗口内持续尝试，保持原有逻辑

### 进程监控策略
- **异常终止**: 记录日志 → 清理浏览器进程 → 重新执行
- **超时控制**: 超过15分钟 → 终止进程 → 重新执行
- **成功条件**: 只有执行完`bot.payment()`才结束
- **重试间隔**: 失败后等待5-10秒再重试

### 日期配置
- **预订月份**: 自动设置为当前月份+6天
- **预订日期**: 自动设置为当前日期+6天
- **更新频率**: 每天自动更新

## 文件结构

```
Scheduler_Bot/
├── scheduler.py          # 主调度器脚本
├── requirements.txt      # Python依赖
├── start.sh             # Linux/macOS启动脚本
├── start.bat            # Windows启动脚本
├── scheduler.log        # 执行日志
└── README.md            # 说明文档
```

## 依赖要求

- Python 3.7+
- psutil >= 5.8.0
- PyYAML >= 6.0

## 安装依赖

```bash
pip install -r requirements.txt
```

## 日志查看

```bash
# 实时查看日志
tail -f scheduler.log

# 查看最后100行日志
tail -n 100 scheduler.log
```

## 注意事项

1. 确保`Smart_Play_Bot`目录存在且包含必要的文件
2. 确保虚拟环境已正确配置
3. 在0-9点执行窗口内会持续尝试，直到预订成功
4. 保持原有的异常处理、超时控制和成功检测逻辑
5. 日期会自动设置为当天+6天，适合预订下周的场地
6. 使用`Ctrl+C`可以停止scheduler

## 示例输出

```
2024-01-15 10:00:00 - INFO - Smart Play Bot Scheduler started
2024-01-15 10:00:00 - INFO - Initializing scheduler...
2024-01-15 10:00:00 - INFO - Current date: 2024-01-15
2024-01-15 10:00:00 - INFO - Target date (+6 days): 2024-01-21
2024-01-15 10:00:00 - INFO - Month: 1, Day: 21
2024-01-15 10:00:00 - INFO - Successfully updated config: booking_month = 1, booking_day = 21
2024-01-15 10:00:00 - INFO - Waiting 50400 seconds until execution time window starts (00:00)
2024-01-16 00:00:00 - INFO - Execution time window started (00:00)
2024-01-16 00:00:01 - INFO - Starting Smart Play Bot
2024-01-16 00:00:15 - WARNING - Bot timed out, will retry
2024-01-16 00:00:20 - INFO - Starting Smart Play Bot
...
```
