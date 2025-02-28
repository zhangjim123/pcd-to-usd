# 在Isaac Sim的脚本编辑器中运行
import os
usd_path = "/home/zhangjim/pointcloud/data_2/merged_pointclouds.usd"

# 检查文件是否存在
print("文件存在:", os.path.exists(usd_path))  # 应为True

# 检查文件权限
print("可读权限:", os.access(usd_path, os.R_OK))  # 应为True

# 尝试二进制读取
try:
    with open(usd_path, "rb") as f:
        f.read(10)
    print("文件可被直接读取")
except Exception as e:
    print("文件读取失败:", e)