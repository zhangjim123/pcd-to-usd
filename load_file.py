from omni.isaac.kit import SimulationApp
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file_path", "-p", type = str, default = None, help = "The path of pointcloud files")

CONFIG = {"headless": False}
sim_app = SimulationApp(CONFIG)

args = parser.parse_args()
if args.file_path == None:
    raise ValueError("Please enter a pointcloud file path")

src_usd = args.file_path

from omni import usd
usd_context = usd.get_context()
usd_context.open_stage(src_usd)

import carb
for _ in range(20):
    sim_app.update()
    carb.log_info(f"强制更新帧数: {_+1}")

stage = usd_context.get_stage()
if stage.GetPrimAtPath("/World"):
    carb.log_info("USD文件加载成功")
else:
    carb.log_error("根Prim /World 未找到")

sim_app.run()
sim_app.close()