import os
import shutil
import subprocess
import sys

# 设置路径
BUILD_DIR = "main.build"
DIST_DIR = "main.dist"
SOURCE_FILE = "main.py"
EXE_FILE = "main.exe"

# 清理构建和输出目录
def clean():
    print("Cleaning build and dist directories...")
    
    # 删除 build 目录
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
        print(f"Removed {BUILD_DIR} directory.")
    
    # 删除 dist 目录
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
        print(f"Removed {DIST_DIR} directory.")
    
    # 删除 main.exe 文件
    if os.path.exists(EXE_FILE):
        os.remove(EXE_FILE)
        print(f"Removed {EXE_FILE} file.")

# 编译构建
def build():
    # 获取虚拟环境中的 Python 路径
    venv_python = shutil.which("python")
    
    if not venv_python:
        print("Python not found in the virtual environment.")
        sys.exit(1)
    
    # 构建命令
    build_command = [
        "nuitka",
        "--standalone",
        "--onefile",
        "--follow-imports",
        "--plugin-enable=numpy",
        SOURCE_FILE
    ]

    # 打印构建命令
    print(f"Running command: {' '.join(build_command)}")
    os.system(' '.join(build_command))

# 主函数，处理命令行参数
def main():
    if len(sys.argv) < 2:
        print("Usage: build.py [build|clean]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "build":
        build()
    elif command == "clean":
        clean()
    else:
        print("Unknown command. Usage: build.py [build|clean]")
        sys.exit(1)

# 调用主函数
if __name__ == "__main__":
    main()
