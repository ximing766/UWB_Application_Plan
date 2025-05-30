# UWB应用计划文档

> 📡 **Ultra-Wideband (UWB) 闸机交易方案设计与应用计划**

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![MkDocs](https://img.shields.io/badge/mkdocs-1.6.1+-green.svg)](https://mkdocs.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 📖 项目简介

本项目是一个专注于UWB技术在闸机交易系统中应用的文档项目。通过详细的方案设计、协议规范和开发指南，为UWB闸机交易系统的开发和实施提供完整的技术文档支持。

### 🎯 主要特性

- **📋 完整的方案设计** - 详细的UWB闸机交易流程设计
- **🔐 认证与安全机制** - 用户身份认证和预读优化方案
- **📡 协议规范** - UWB通信协议和数据格式定义
- **🚀 开发指南** - 完整的开发环境搭建和API使用指南
- **💡 示例代码** - 丰富的实际应用示例
- **📚 在线文档** - 基于MkDocs的现代化文档站点

## 🚀 快速开始

### 环境要求

- Python 3.11 或更高版本
- Git

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/ximing766/UWB_Application_Plan.git
   cd UWB_Application_Plan
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/macOS
   source .venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -e .
   ```

4. **启动文档服务器**
   ```bash
   python main.py serve
   ```

5. **访问文档**
   
   打开浏览器访问 http://127.0.0.1:8000

## 🛠️ 使用方法

### 命令行工具

项目提供了便捷的命令行工具来管理文档：

```bash
# 显示帮助信息
python main.py --help

# 启动开发服务器
python main.py serve

# 指定端口启动服务器
python main.py serve --port 8080

# 构建静态文档
python main.py build

# 检查文档结构
python main.py check

# 初始化项目结构
python main.py init
```

### 传统MkDocs命令

你也可以直接使用MkDocs命令：

```bash
# 启动开发服务器
mkdocs serve

# 构建文档
mkdocs build

# 部署到GitHub Pages
mkdocs gh-deploy
```

## 📁 项目结构

```
UWB_Application_Plan/
├── docs/                           # 文档源文件
│   ├── ApplicationPlan/            # 应用计划文档
│   │   └── UwbApplicationPlanDesign_V1.1.md
│   ├── protocol/                   # 协议文档
│   │   ├── uwb-protocol.md
│   │   └── data-format.md
│   ├── guide/                      # 开发指南
│   │   ├── quick-start.md
│   │   └── setup.md
│   ├── api/                        # API文档
│   │   └── reference.md
│   ├── examples/                   # 示例代码
│   │   ├── basic.md
│   │   └── advanced.md
│   ├── images/                     # 图片资源
│   └── index.md                    # 首页
├── .venv/                          # 虚拟环境
├── main.py                         # 文档管理工具
├── mkdocs.yml                      # MkDocs配置文件
├── pyproject.toml                  # 项目配置
├── README.md                       # 项目说明
└── uv.lock                         # 依赖锁定文件
```

## 📚 文档内容

### 🏗️ 应用计划
- **闸机交易方案设计** - 完整的UWB闸机交易流程设计，包括入站认证、预读方案、交易流程等

### 📋 协议文档
- **UWB通信协议** - UWB设备间通信协议规范
- **数据格式规范** - 数据包格式和编码规范

### 🚀 开发指南
- **快速开始** - 快速上手开发指南
- **环境搭建** - 开发环境配置说明
- **API参考** - 完整的API接口文档

### 💡 示例代码
- **基础示例** - 基本功能实现示例
- **高级应用** - 复杂场景应用示例

## 🔧 开发

### 开发环境设置

1. **安装开发依赖**
   ```bash
   pip install -e ".[dev]"
   ```

2. **代码格式化**
   ```bash
   black .
   ```

3. **代码检查**
   ```bash
   flake8 .
   mypy .
   ```

### 添加新文档

1. 在 `docs/` 目录下创建新的Markdown文件
2. 在 `mkdocs.yml` 的 `nav` 部分添加导航链接
3. 使用 `python main.py serve` 预览效果

### 自定义样式

- CSS样式文件：`docs/stylesheets/extra.css`
- 主题配置：`mkdocs.yml` 中的 `theme` 部分

## 🚀 部署

### GitHub Pages

```bash
# 部署到GitHub Pages
mkdocs gh-deploy
```

### 手动部署

```bash
# 构建静态文件
python main.py build

# 将site/目录内容部署到你的服务器
```

## 🤝 贡献指南

我们欢迎任何形式的贡献！请遵循以下步骤：

1. **Fork 本项目**
2. **创建特性分支**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **提交更改**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **推送到分支**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **开启 Pull Request**

### 贡献类型

- 📝 文档改进
- 🐛 错误修复
- ✨ 新功能
- 🎨 界面优化
- 📚 示例代码

## 📄 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## 📞 联系我们

- 📧 **Email**: ximing766@gmail.com
- 🐙 **GitHub**: [UWB_Application_Plan](https://github.com/ximing766/UWB_Application_Plan.git)
- 🐛 **Issues**: [报告问题](https://github.com/ximing766/UWB_Application_Plan/issues)

## 🙏 致谢

感谢所有为本项目做出贡献的开发者和用户！

- [MkDocs](https://mkdocs.org/) - 静态站点生成器
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) - 现代化主题
- [Python](https://python.org/) - 编程语言

---

<div align="center">
  <strong>UWB应用计划文档项目</strong><br>
  <em>让UWB技术文档更加专业和易用</em><br><br>
  <sub>Built with ❤️ by Kewei@QLL</sub>
</div>