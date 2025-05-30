#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UWB应用计划文档管理工具

这个工具用于管理UWB应用计划的文档，包括：
- 启动MkDocs开发服务器
- 构建文档站点
- 文档预览和管理
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def serve_docs(host="127.0.0.1", port=8000):
    """
    启动MkDocs开发服务器
    
    Args:
        host (str): 服务器主机地址
        port (int): 服务器端口
    """
    try:
        print(f"🚀 启动文档服务器: http://{host}:{port}")
        subprocess.run(["mkdocs", "serve", "-a", f"{host}:{port}"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动服务器失败: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ 未找到mkdocs命令，请确保已安装MkDocs")
        print("💡 安装命令: pip install mkdocs mkdocs-material")
        sys.exit(1)


def build_docs(output_dir="site"):
    """
    构建文档站点
    
    Args:
        output_dir (str): 输出目录
    """
    try:
        print(f"🔨 构建文档到: {output_dir}")
        cmd = ["mkdocs", "build"]
        if output_dir != "site":
            cmd.extend(["-d", output_dir])
        subprocess.run(cmd, check=True)
        print("✅ 文档构建完成")
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ 未找到mkdocs命令，请确保已安装MkDocs")
        sys.exit(1)


def check_docs():
    """
    检查文档结构和配置
    """
    print("🔍 检查文档结构...")
    
    # 检查必要文件
    required_files = [
        "mkdocs.yml",
        "docs/index.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 缺少必要文件:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ 文档结构检查通过")
    return True


def init_project():
    """
    初始化项目结构
    """
    print("🎯 初始化UWB应用计划文档项目...")
    
    # 创建必要的目录
    dirs_to_create = [
        "docs/images",
        "docs/protocol",
        "docs/guide",
        "docs/api",
        "docs/examples"
    ]
    
    for dir_path in dirs_to_create:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"📁 创建目录: {dir_path}")
    
    print("✅ 项目初始化完成")


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(
        description="UWB应用计划文档管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python main.py serve              # 启动开发服务器
  python main.py build              # 构建文档
  python main.py check              # 检查文档结构
  python main.py init               # 初始化项目
  python main.py serve --port 8080  # 指定端口启动服务器
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # serve命令
    serve_parser = subparsers.add_parser("serve", help="启动开发服务器")
    serve_parser.add_argument("--host", default="127.0.0.1", help="服务器主机地址")
    serve_parser.add_argument("--port", type=int, default=8000, help="服务器端口")
    
    # build命令
    build_parser = subparsers.add_parser("build", help="构建文档")
    build_parser.add_argument("-d", "--output-dir", default="site", help="输出目录")
    
    # check命令
    subparsers.add_parser("check", help="检查文档结构")
    
    # init命令
    subparsers.add_parser("init", help="初始化项目结构")
    
    args = parser.parse_args()
    
    if not args.command:
        # 默认行为：显示帮助信息
        parser.print_help()
        print("\n🎯 UWB应用计划文档项目")
        print("📖 这是一个用于管理UWB应用计划文档的工具")
        return
    
    # 执行对应命令
    if args.command == "serve":
        if check_docs():
            serve_docs(args.host, args.port)
    elif args.command == "build":
        if check_docs():
            build_docs(args.output_dir)
    elif args.command == "check":
        check_docs()
    elif args.command == "init":
        init_project()


if __name__ == "__main__":
    main()
