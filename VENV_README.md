# Python虚拟环境使用说明

## 虚拟环境管理脚本

项目使用统一的 `activate_venv.sh` 脚本来管理虚拟环境，支持自动配置、依赖安装和环境激活。

## 快速开始

### 首次使用 - 一键配置环境
```bash
# 配置虚拟环境并安装所有依赖
source ./activate_venv.sh setup
```

这个命令会自动：
- 创建根目录和 Smart_Play_Bot 虚拟环境
- 安装所有必要的依赖包
- 解决兼容性问题（urllib3、PyYAML等）
- 验证安装结果

### 激活虚拟环境

- 激活根目录虚拟环境：
```bash
source ./activate_venv.sh
# 或者简写
source ./activate_venv.sh root
```

- 激活 Smart_Play_Bot 专用虚拟环境（推荐）：
```bash
source ./activate_venv.sh smart
```

## 脚本功能详解

### 1. 环境配置模式 (`setup`)
```bash
source ./activate_venv.sh setup
```
- 自动检测 Python3 环境
- 创建缺失的虚拟环境
- 安装所有依赖包
- 安装兼容性包解决版本冲突
- 验证关键模块安装状态

### 2. 虚拟环境激活
- **root 模式**：激活项目根目录虚拟环境
- **smart 模式**：激活 Smart_Play_Bot 专用虚拟环境

### 3. 自动依赖管理
脚本会自动：
- 升级 pip 到最新版本
- 安装 `requirements.txt` 中的依赖
- 安装兼容性包：
  - `urllib3==1.26.18` - 解决 macOS LibreSSL 兼容性问题
  - `PyYAML==6.0.1` - 确保 YAML 模块正常工作
- 验证安装结果

## 已安装的依赖包

两个虚拟环境都安装了相同的依赖包：

- **selenium==4.24.0** - 网页自动化工具
- **requests** - HTTP请求库
- **pandas** - 数据处理库
- **numpy** - 数值计算库
- **PyYAML** - YAML文件处理库

## 退出虚拟环境

当您完成工作后，可以退出虚拟环境：
```bash
deactivate
```

## 重新配置环境

如果需要重新安装依赖或创建虚拟环境：
```bash
source ./activate_venv.sh setup
```

## 注意事项

1. **首次使用**：必须先运行 `source ./activate_venv.sh setup` 配置环境
2. **每次使用**：使用项目前都需要先激活虚拟环境
3. **推荐环境**：推荐使用 Smart_Play_Bot 专用虚拟环境，避免依赖冲突
4. **版本控制**：虚拟环境文件夹已添加到 `.gitignore` 中
5. **新依赖**：安装新包前确保虚拟环境已激活
6. **pip 命令**：如果直接使用 `pip` 失败，请使用 `python -m pip`

## 项目结构

```
Custom_Web_Bot/
├── venv/                    # 项目根目录虚拟环境
├── activate_venv.sh         # 统一虚拟环境管理脚本
│                           # 支持: root/smart/setup 模式
├── requirements.txt         # 根目录依赖列表
├── Smart_Play_Bot/
│   ├── venv/               # Smart_Play_Bot 专用虚拟环境
│   ├── smart_play_bot.py   # 主程序
│   ├── requirements.txt    # 依赖列表
│   └── ...
└── VENV_README.md          # 本说明文件
```

## 推荐使用方式

**推荐使用 Smart_Play_Bot 专用虚拟环境**，因为：
1. 它是专门为该模块配置的
2. 依赖包版本更精确匹配
3. 避免与其他模块的依赖冲突
4. 自动处理兼容性问题

## 故障排除

### 常见问题

#### 1. 虚拟环境未找到
```bash
# 运行配置命令
source ./activate_venv.sh setup
```

#### 2. 依赖安装失败
```bash
# 重新配置环境
source ./activate_venv.sh setup

# 或手动安装
source ./activate_venv.sh smart
python -m pip install -r Smart_Play_Bot/requirements.txt
python -m pip install urllib3==1.26.18 PyYAML==6.0.1
```

#### 3. Python 命令问题
脚本会自动检测并使用可用的 Python 命令（python 或 python3）

#### 4. pip 命令问题
如果直接使用 `pip` 命令失败，请使用 `python -m pip`：
```bash
# 激活环境后
source ./activate_venv.sh smart

# 使用 python -m pip 而不是直接使用 pip
python -m pip install package_name
python -m pip list
python -m pip --version
```

#### 5. 虚拟环境链接问题
如果虚拟环境中的命令链接到错误的路径：
```bash
# 删除有问题的虚拟环境
rm -rf Smart_Play_Bot/venv

# 重新运行配置
source ./activate_venv.sh setup
```

#### 6. 模块导入错误
如果出现 `ModuleNotFoundError`：
```bash
# 确保在正确的虚拟环境中
source ./activate_venv.sh smart

# 验证模块安装
python -c "import yaml; print('PyYAML 可用')"
python -c "import selenium; print('Selenium 可用')"
```

## 使用流程

1. **首次使用**：`source ./activate_venv.sh setup`
2. **日常使用**：`source ./activate_venv.sh smart`
3. **开发完成**：`deactivate`
4. **重新配置**：`source ./activate_venv.sh setup`

## 手动安装依赖（备用方案）

如果自动安装失败，可以手动安装：

### 方法1：使用 activate_venv.sh 脚本
```bash
# 重新配置环境
source ./activate_venv.sh setup
```

### 方法2：完全手动安装
```bash
# 1. 创建虚拟环境
cd Smart_Play_Bot
python3 -m venv venv

# 2. 激活环境
source venv/bin/activate

# 3. 升级 pip
python -m pip install --upgrade pip

# 4. 安装依赖
python -m pip install -r requirements.txt

# 5. 安装兼容性包
python -m pip install urllib3==1.26.18
python -m pip install PyYAML==6.0.1

# 6. 验证安装
python -c "import yaml; print('PyYAML 安装成功')"
python -c "import selenium; print('Selenium 安装成功')"
python -c "import pandas; print('Pandas 安装成功')"
python -c "import numpy; print('NumPy 安装成功')"
```

### 方法3：修复现有虚拟环境
如果虚拟环境存在但有问题：
```bash
# 1. 删除有问题的虚拟环境
rm -rf Smart_Play_Bot/venv

# 2. 重新创建
cd Smart_Play_Bot
python3 -m venv venv

# 3. 激活并安装依赖
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install urllib3==1.26.18 PyYAML==6.0.1
```

## 验证安装

安装完成后，验证所有模块是否可用：
```bash
# 激活环境
source ./activate_venv.sh smart

# 测试导入
python -c "
import yaml
import selenium
import pandas
import numpy
import requests
print('所有模块导入成功！')
"
```

现在您可以开始使用项目了！记得先运行 `source ./activate_venv.sh setup` 配置环境，然后使用 `source ./activate_venv.sh smart` 激活 Smart_Play_Bot 虚拟环境。
