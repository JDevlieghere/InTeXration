# Installation

 - [Prerequisites](#prerequisites)
 - [Installing](#installing)
 - [Starting the Server](#starting-the-server)

## Prerequisites

InTeXration requires:

- Python 3
- pdflatex (part of TexX Live)
- pip

We're assuming `python3` refers to the right version. You can check your python version using the `python3 --version
` command. It should say something like `Python 3.x.x`. Use pip to install the required python packages:

```bash
pip install -r requirements.txt
```

Installing the full version of TeX Live is recommended. If you'll be running
InTeXration on Ubuntu, [this repository](https://github.com/scottkosty/install-
tl-ubuntu) might come in handy.


## Installing
Run the `setup.py` file as illustrated below:
```bash
python3 setup.py install
```

## Configuring

[This document](https://github.com/JDevlieghere/InTeXration/blob/master/docs/config.md) explains how to configure your InTeXration server.

## Starting the Server
Starting the server is as easy as running the InTeXration module. However, if you
want to run InTeXration in the background, you can use the `nohup` command.

```bash
nohup python3 -m intexration > /dev/null 2>&1 &
```
You will be show the process id, which you will need in order to stop the
server, if necessary.