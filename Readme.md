# Ai system for CCTV

## Python modules

Create a virtualenv for the project:

```bash
python3 -m venv env
source env/bin/activate
```

Then you need to install the pip modules to execute the scripts:

```bash
pip install -r requirements.txt
```

Edit the *config/config.ini* file to add the path of the folder you want to watch and the optional telegram token for the notification:

```bash
cp scripts/config/config.ini.sample scripts/config/config.ini
```

Execute the script to watch the folder:

```bash
cd scripts
python3 main.py
```

Sample output:
![Sample image](sample.jpeg)

## Prerequisites

In order to scan the images for people, you need to have an object detection model available. There are adaptors in the `scripts/models` directory. Check those files if you want to use a different model. I'm using the caffe implementation of [MobileSSD](https://github.com/chuanqi305/MobileNet-SSD) for detections in the daylight, and [YOLO](https://pjreddie.com/darknet/yolo/).
