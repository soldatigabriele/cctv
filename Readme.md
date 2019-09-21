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

Edit the .env file to add the path of the folder you want to watch and the optional telegram token for the notification:

```bash
cp scripts/.env_example scripts/.env
```

Execute the script to watch the folder:

```bash
cd scripts
python main.py
```

## Prerequisites

In order to scan the images for people, you need to have a server accepting the image and a model that scans it. For convenience we will use [this docker image](https://hub.docker.com/r/codait/max-object-detector).

```bash
git clone https://github.com/IBM/MAX-Object-Detector.git object_detector
cd object_detector
docker build -t object-detector .
docker run -it -p 5000:5000 -e DISABLE_WEB_APP=true object-detector
```
