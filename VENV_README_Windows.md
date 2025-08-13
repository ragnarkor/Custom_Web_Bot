# Windows 系统使用说明

## 项目概述

这是一个包含多个Python项目的Web Bot自动化系统，包含以下主要组件：

- **根目录**: 主要依赖包和通用功能
- **Smart_Play_Bot**: 智能游戏预订机器人
- **Scheduler_Bot**: 任务调度机器人

## 系统要求

- Windows 10/11 或 Windows Server 2016+
- Python 3.8 或更高版本
- 确保Python已添加到系统PATH环境变量中

## 快速开始

### 使用统一管理脚本

双击运行 `venv_manager.bat` 文件，这是一个统一的虚拟环境管理工具，提供以下功能：

- **选项 1**: 安装所有虚拟环境 (推荐首次使用)
- **选项 2**: 激活根目录虚拟环境
- **选项 3**: 激活Smart_Play_Bot虚拟环境
- **选项 4**: 激活Scheduler_Bot虚拟环境
- **选项 5**: 清理所有虚拟环境
- **选项 6**: 退出程序



## 虚拟环境管理

### 激活虚拟环境
- 双击对应的 `.bat` 文件
- 或在命令提示符中运行对应的 `.bat` 文件

### 验证激活状态
激活成功后，命令提示符前会显示 `(venv)` 标识。

### 退出虚拟环境
在激活的虚拟环境中输入：
```cmd
deactivate
```

### 查看已安装的包
```cmd
pip list
```

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
├── venv_manager.bat               # 统一虚拟环境管理器
└── README_Windows.md              # 本文件
```

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

## 常见问题

### Q: 提示"Python不是内部或外部命令"
**A**: 请确保Python已正确安装并添加到系统PATH中。

### Q: 虚拟环境激活失败
**A**: 请先运行 `install_venv_root.bat` 创建虚拟环境。

### Q: 依赖安装失败
**A**: 检查网络连接，或尝试使用国内镜像源：
```cmd
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt
```

### Q: 权限不足
**A**: 以管理员身份运行命令提示符。

## 更新依赖

如需更新依赖包，可以：

1. 激活对应的虚拟环境
2. 运行更新命令：
```cmd
pip install --upgrade -r requirements.txt
```

## 技术支持

如遇到问题，请检查：
1. Python版本是否符合要求
2. 虚拟环境是否正确创建
3. 依赖包是否完整安装
4. 系统权限是否足够

---

**注意**: 首次使用请务必先运行 `venv_manager.bat` 并选择选项 1 安装所有虚拟环境。
