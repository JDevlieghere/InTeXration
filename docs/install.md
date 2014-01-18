# Installation

## Prerequisites

InTeXration requires:

- Python 3
- pdflatex (part of TexX Live)
- pip

Use pip to install the required python packages:

```bash
pip install -r requirements.txt
```

Installing the full version of TeX Live is recommended. If you'll be running
InTeXration on Ubuntu, [this repository](https://github.com/scottkosty/install-
tl-ubuntu) might come in handy.

## Configuring

Configuration is done using command line arguments. The following options are available.


```bash
  -h, --help      show this help message and exit
  -host HOST      Change the hostname
  -port PORT      Change the port
  -add ADD        Add API key
  -remove REMOVE  Remove API key
  -list           List API keys
```

To set host to `localhost` and port to `8000` run
```bash
python -m intexration -host localhost -port 8000
```


## Installation
Run the `setup.py` file as illustrated below:
```bash
python setup.py install
```

## Starting the server
Starting the server is as easy as running the InTeXration module. However, if you
want to run InTeXration in the background, you can use the `nohup` command.

```bash
nohup python -m intexration > /dev/null 2>&1 &
```
You will be show the process id, which you will need in order to stop the
server, if necessary.