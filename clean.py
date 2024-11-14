import os
import shutil

def clean_output_directory(output_directory: str) -> None:
    """
    清理指定的输出目录，删除其中的所有文件。
    
    参数:
    - output_directory (str): 输出目录的路径。
    """
    # 检查目录是否存在
    if os.path.exists(output_directory):
        # 遍历目录中的文件并删除
        for filename in os.listdir(output_directory):
            file_path = os.path.join(output_directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"已删除文件: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # 删除子目录及其内容
                    print(f"已删除目录: {file_path}")
            except Exception as e:
                print(f"删除文件 {file_path} 时发生错误: {e}")
    else:
        print(f"目录 {output_directory} 不存在。")

# 使用示例
if __name__ == "__main__":
    output_dir = "image/output"
    clean_output_directory(output_dir)
