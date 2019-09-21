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
python monitor_folder.py
```
