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
cp scripts/config.ini.sample scripts/config/config.ini
```

Execute the script to watch the folder:

```bash
cd scripts
python3 main.py
```

Sample output:
![Sample image](sample.jpeg)

## Prerequisites

In order to scan the images for people, you need to have a server accepting the image and a model that scans it. For convenience we will use [this docker image](https://hub.docker.com/r/codait/max-object-detector).

```bash
git clone https://github.com/IBM/MAX-Object-Detector.git object_detector
cd object_detector
docker build -t object-detector .
docker run -it -p 5000:5000 -e DISABLE_WEB_APP=true object-detector
```
