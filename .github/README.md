# GitHub工作流配置

本目录包含UWB_Application_Plan项目的GitHub Actions工作流配置和相关GitHub设置文件。

## 工作流文件

### 1. 文档部署 (`workflows/deploy-docs.yml`)

此工作流负责构建MkDocs文档并将其部署到GitHub Pages。

**触发条件**：
- 推送到`main`分支
- 手动触发（workflow_dispatch）

**主要步骤**：
1. 检出代码
2. 设置Python环境
3. 安装依赖
4. 构建MkDocs文档
5. 部署到GitHub Pages（仅在`main`分支上）

### 2. 代码质量检查 (`workflows/code-quality.yml`)

此工作流运行代码质量检查工具。

**触发条件**：
- 推送到`main`分支
- 创建Pull Request到`main`分支

**主要步骤**：
1. 检出代码
2. 设置Python环境
3. 安装依赖
4. 运行Black格式检查
5. 运行Flake8代码检查
6. 运行MyPy类型检查

### 3. 测试 (`workflows/tests.yml`)

此工作流运行项目测试。

**触发条件**：
- 推送到`main`分支
- 创建Pull Request到`main`分支

**主要步骤**：
1. 检出代码
2. 设置Python环境（测试多个Python版本）
3. 安装依赖
4. 运行Pytest测试
5. 上传测试覆盖率报告

## 其他配置文件

### Dependabot配置 (`dependabot.yml`)

配置Dependabot自动检查和更新项目依赖。

### CODEOWNERS文件

定义代码库中不同部分的负责人，用于自动分配代码审查者。

### Issue模板

提供标准化的问题报告模板：
- `bug_report.md`: 错误报告模板
- `feature_request.md`: 功能请求模板
- `documentation_improvement.md`: 文档改进请求模板

### Pull Request模板

`pull_request_template.md`提供标准化的拉取请求格式。

## 使用说明

### 手动触发文档部署

1. 前往GitHub仓库页面
2. 点击"Actions"选项卡
3. 从左侧列表选择"Deploy MkDocs"工作流
4. 点击"Run workflow"按钮
5. 选择分支并点击"Run workflow"确认

### 配置GitHub Pages

确保在仓库设置中正确配置GitHub Pages：

1. 前往仓库"Settings" > "Pages"
2. 在"Source"部分，选择"gh-pages"分支和"/ (root)"文件夹
3. 点击"Save"

## 故障排除

如果工作流失败，请检查：

1. 依赖项是否正确安装
2. MkDocs配置文件是否有效
3. 测试是否通过
4. 代码是否符合格式和类型检查要求