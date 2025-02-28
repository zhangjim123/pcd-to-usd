from pxr import Usd, UsdGeom, Gf, Kind
import open3d as o3d
import numpy as np
import os
from tqdm import tqdm  # 进度条支持
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file_path", "-p", type = str, default = None, help = "The path of pointcloud files")
parser.add_argument("--size", "-s", type = float, default = 0.01, help = "The size of the usd point")

def pcds_to_usd(pcd_dir, output_usd, point_size=0.01):
    """
    将目录下的PCD文件合并为单个USD文件
    参数：
        pcd_dir: 包含PCD文件的输入目录
        output_usd: 输出USD文件路径
        point_size: 点云显示直径（单位：米）
    """
    # 初始化USD场景
    stage = Usd.Stage.CreateNew(output_usd)
    stage.GetRootLayer().comment = "#usda 1.0\n"
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    
    # 创建根Xform用于组织所有点云
    root_xform = UsdGeom.Xform.Define(stage, "/World/PointClouds")
    
    # 获取目录下所有PCD文件
    pcd_files = [f for f in os.listdir(pcd_dir) if f.endswith(".pcd")]
    
    for idx, pcd_file in enumerate(tqdm(pcd_files, desc="Processing PCDs")):
        # 生成唯一Prim路径（示例：/World/PointClouds/Frame_0001）
        prim_path = f"/World/PointClouds/Frame_{idx:04d}"
        
        # 读取点云数据
        pcd = o3d.io.read_point_cloud(os.path.join(pcd_dir, pcd_file))
        points = np.asarray(pcd.points)
        
        if not np.isfinite(points).all():
            points = np.nan_to_num(points)
            print(f"警告: {pcd_file} 中存在非法坐标，已自动清理")
        
        # 定义Points Prim
        point_cloud = UsdGeom.Points.Define(stage, prim_path)
        point_cloud.CreatePointsAttr().Set([Gf.Vec3f(p[0], -p[1], p[2]) for p in points])
        
        # 设置点大小（统一值）
        point_cloud.CreateWidthsAttr().Set([point_size])
        
        # 处理颜色信息
        if pcd.has_colors():
            colors = np.asarray(pcd.colors)
            if colors.max() > 1.0 or colors.min() < 0.0:
                colors = np.clip(colors, 0.0, 1.0)
            if np.isnan(colors).any():
                colors = np.nan_to_num(colors)
                print(f"警告: {pcd_file} 中存在非法颜色值，已自动清理")
            color_primvar = point_cloud.CreateDisplayColorPrimvar(
                interpolation=UsdGeom.Tokens.vertex
            )
            color_primvar.Set([Gf.Vec3f(c[0], c[1], c[2]) for c in colors])
        
        # 设置时间采样（可选）
        # point_cloud.GetPrim().SetAttribute("time", idx)  # 如果需要时间序列
        
        # 设置Prim元数据
        Usd.ModelAPI(point_cloud).SetKind(Kind.Tokens.component)
        safe_filename = pcd_file.encode("utf-8", "ignore").decode("utf-8")
        point_cloud.GetPrim().SetMetadata("comment", f"Source: {safe_filename}")

    # 保存USD文件
    stage.GetRootLayer().Save()
    print(f"Successfully exported {len(pcd_files)} PCDs to {output_usd}")

if __name__ == "__main__":
    args = parser.parse_args()
    if args.file_path == None:
        raise ValueError("please enter a file path")
    # 配置参数
    config = {
        "pcd_dir": args.file_path,  # PCD文件目录
        "output_usd": args.file_path + "/merged_pointclouds.usd",
        "point_size": args.size
    }
    
    # 执行转换
    pcds_to_usd(**config)