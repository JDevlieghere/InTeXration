# Installation

 - [Overview](#overview)
 - [Prerequisites](#prerequisites)
 - [Installing](#installing)
 - [Starting the Server](#starting-the-server)

## Overview

This guide is written as generally as possible to cover multiple GNU/Linux distributions. However, it has currently only been tested with the following versions:

 - Ubuntu 12.04 LTS
 - Ubuntu 13.10

## Prerequisites

InTeXration requires:

 - Python 3
 - pdflatex (part of TeX Live)
 - pip
 - The packages specified in requirements.txt

### Python 3

We're assuming that `python3` refers to the right version. You can check your python version using the `python3 -V` command. It should say something like `Python 3.3.2+`.

### Pdflatex

Installing the full version of TeX Live is recommended. If you'll be running
InTeXration on Ubuntu, [this repository](https://github.com/scottkosty/install-
tl-ubuntu) might come in handy.

### Pip and Packages

Pip is a package management system for managing and installing packages in Python. Please note that is supports both versions on Python. Since this project is using Python 3 make sure you have the right version or configuration. If you're using InTeXration on Ubuntu, the easiest way is to install `python3-pip`. We'll assume that `pip` for Python 3 is called `pip3` from now on.

Installing `python3-pip` on Ubuntu 12.10 or later:
```bash
$ sudo apt-get install python3-pip
```
If you're on an earlier version of Ubuntu (12.04 LTS for example) you can make use of the `python3-setuptools` package:
```bash
$ sudo aptitude install python3-setuptools
$ sudo easy_install3 pip
```

Installing the requirements from the text file:
```bash
$ sudo pip3 install -r requirements.txt
```

Once all prerequisites are installed, you're ready to install InTeXration itself.

## Installing

Before installing the application you will have to create a user named `intexration`. Make sure it receives a directory called `intexration` in the `/home` folder.

```bash
$ sudo adduser --disabled-login --gecos 'InTeXration' intexration
$ cd /home/intexration
```

No return to the root of the repository to start the installation process. Installing the application itself is pretty easy. Just run the `setup.py` file as illustrated below:

```bash
$ sudo python3 setup.py install
```

## Configuring

As explained in [this document](https://github.com/JDevlieghere/InTeXration/blob/master/docs/config.md) some files are necessary for InTeXration to run properly. Summarized: InTeXration can create these automatically for you if it has the right privileges. Make sure InTeXration can create directories and files in the folder `/home/intexration`. A possible way to do so is starting it as the root user.

```bash
$ sudo python3 -m intexration
```

If you don't notice any I/O-related issues, the installation in now complete.

## Starting the Server

Starting the server is as easy as running the InTeXration module. Please do so outside of the root of the repository. Otherwise Python might choose to run the copy located there rather than the one installed as a module.

```bash
$ python3 -m intexration
```

However, if you want to run InTeXration in the background, you can do so using the `nohup` command.

```bash
$ nohup python3 -m intexration > /dev/null 2>&1 &
```

You will be show the process id, which you will need in order to stop the
server, if necessary.
