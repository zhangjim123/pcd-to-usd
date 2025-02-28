# pcd-to-usd
A sample repository to change a set of pcd pointclouds to a usd
file and load it to isaac-sim monitor. The running of the code is easy
```bash
git clone https://github.com/zhangjim123/pcd-to-usd.git
conda create -n change python=3.8
conda activate change
pip install -r requirements.txt
```
To change a set of pcd file into a single usd file, use
```bash
python change_file.py -p <pcd-filepath> -s <size-num>
# e.g. python change_file.py -p /home/zhangjim/pointcloud/data -s 0.01
# This instruction change all the pcd files under /home/zhangjim/pointcloud/data
# into a single usd file called /home/zhangjim/pointcloud/data/merge_pointclouds.usd
# with a point size of 0.01 and an upward axis of y
```
To activate the monitor, use
```bash
cd ~/isaac-sim-4.5.0
# This can be changed into your own isaac sim path
./python.sh <load_file-path>
# load_file-path is the absolute path of load_file.py
```
