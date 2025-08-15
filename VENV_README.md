# Python虚拟环境与依赖管理说明

---

## 目录
- [macOS/Linux 使用方法](#macoslinux-使用方法)
- [Windows 使用方法](#windows-使用方法)
- [常见问题与故障排除](#常见问题与故障排除)
- [项目结构](#项目结构)
- [依赖包说明](#依赖包说明)

---

## macOS/Linux 使用方法

### 1. 一键配置所有虚拟环境和依赖
```bash
source ./venv_manager_mac.sh setup
# 或
source ./venv_manager_mac.sh all
```
- 自动为根目录、Smart_Play_Bot、Scheduler_Bot 创建虚拟环境并安装依赖。

### 2. 激活虚拟环境
- 激活根目录虚拟环境：
  ```bash
  source ./venv_manager_mac.sh
  # 或 source ./venv_manager_mac.sh root
  ```
- 激活 Smart_Play_Bot 虚拟环境：
  ```bash
  source ./venv_manager_mac.sh smart
  ```
- 激活 Scheduler_Bot 虚拟环境：
  ```bash
  source ./venv_manager_mac.sh scheduler
  ```

### 3. 退出虚拟环境
```bash
deactivate
```

### 4. 查看已安装的包
```bash
pip list
```

---

## Windows 使用方法

### 1. 一键管理所有虚拟环境
- 双击运行 `venv_manager_win.bat`，根据菜单选择：
  - 1：安装所有虚拟环境
  - 2：激活根目录虚拟环境
  - 3：激活 Smart_Play_Bot 虚拟环境
  - 4：激活 Scheduler_Bot 虚拟环境
  - 5：清理所有虚拟环境

### 2. 退出虚拟环境
在激活的命令行窗口输入：
```cmd
deactivate
```

### 3. 查看已安装的包
```cmd
pip list
```

---

## 常见问题与故障排除

### 1. Python 未找到
- macOS/Linux: 请确保 `python3` 已安装。
- Windows: 请确保 Python 已安装并添加到 PATH。

### 2. 虚拟环境激活失败
- macOS/Linux: 运行 `source ./venv_manager_mac.sh setup` 重新配置。
- Windows: 运行 `venv_manager_win.bat` 选择 1 重新安装。

### 3. 依赖安装失败
- 检查网络连接，或尝试使用国内镜像源：
  ```bash
  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt
  ```

### 4. 权限不足
- Windows: 以管理员身份运行命令提示符。
- macOS/Linux: 使用有权限的用户。

### 5. pip 命令问题
- 推荐使用 `python -m pip` 或 `python3 -m pip`。

### 6. 虚拟环境链接问题
- 删除有问题的虚拟环境文件夹，重新运行配置命令。

### 7. 验证依赖安装
```bash
python -c "import yaml, selenium, pandas, numpy, requests; print('所有模块导入成功！')"
```

---

## 项目结构

```
Custom_Web_Bot/
├── venv/                          # 根目录虚拟环境
├── Smart_Play_Bot/
│   ├── venv/                      # Smart_Play_Bot虚拟环境
│   ├── requirements.txt           # Smart_Play_Bot依赖
│   └── ...
├── Scheduler_Bot/
│   ├── venv/                      # Scheduler_Bot虚拟环境
│   ├── requirements.txt           # Scheduler_Bot依赖
│   └── ...
├── requirements.txt                # 根目录依赖
├── venv_manager_mac.sh            # macOS/Linux统一虚拟环境管理脚本
├── venv_manager_win.bat           # Windows统一虚拟环境管理器
└── VENV_README.md                 # 本说明文件
```

---

## 依赖包说明

### 根目录依赖
- selenium: Web自动化框架
- requests: HTTP请求库
- pandas: 数据处理库
- numpy: 数值计算库
- 其他网络和数据处理相关包

### Smart_Play_Bot依赖
- selenium: Web自动化
- requests: HTTP请求
- pandas: 数据处理
- numpy: 数值计算
- PyYAML: YAML配置文件处理

### Scheduler_Bot依赖
- psutil: 系统和进程监控
- PyYAML: YAML配置文件处理

---

**注意**：首次使用请务必先按对应系统方法一键配置所有虚拟环境和依赖。
