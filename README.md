# yolov5-head-detector
---
## How to use
Three params you need input:

1. `--source` (`usb` or `csi` or `video_path`)
2. `--device` (if you choose usb, you need choose device number)
3. `--thresh` (warning number, if detect number below threshhold, it will warning)
- Run usb camera as input 
```shell
python demo.py --source usb --device 0 --thresh 30
```
- Run csi camera as input 
```shell
python demon.py --source csi --thresh 30
```
- Run video as input 
```shell
python demo.py --source video_path --thresh 30
```