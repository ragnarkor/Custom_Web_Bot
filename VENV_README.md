# Python虚拟环境使用说明

## 虚拟环境已创建完成！

项目包含两个已创建的虚拟环境：

1. **项目根目录虚拟环境** (`Custom_Web_Bot/venv/`) - 适用于整个项目
2. **Smart_Play_Bot 专用虚拟环境** (`Smart_Play_Bot/venv/`) - 专门用于 Smart_Play_Bot 模块（推荐）

现在使用一个统一的脚本在项目根目录进行激活。

## 使用方法（重要：使用 source 激活到当前 shell）

- 激活根目录虚拟环境：
```bash
source ./activate_venv.sh
# 或
source ./activate_venv.sh root
```

- 激活 Smart_Play_Bot 专用虚拟环境（推荐）：
```bash
source ./activate_venv.sh smart
```

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

## 注意事项

1. 每次使用项目前都需要先激活虚拟环境
2. 推荐使用 `Smart_Play_Bot/venv/` 虚拟环境，因为它是专门为该模块配置的
3. 虚拟环境文件夹 `venv/` 已添加到 `.gitignore` 中，不会被提交到版本控制
4. 如果需要安装新的依赖包，请确保虚拟环境已激活，然后使用 `pip install package_name`

## 项目结构

```
Custom_Web_Bot/
├── venv/                    # 项目根目录虚拟环境
├── activate_venv.sh         # 统一虚拟环境激活脚本（root/smart）
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

现在您可以开始使用项目了！记得先在根目录用 `source ./activate_venv.sh smart` 激活。
