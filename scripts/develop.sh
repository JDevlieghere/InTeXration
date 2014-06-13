#!/usr/bin/env bash

# Fetch latest version from git
git pull origin/develop

# Install using setup.py
sudo python3 setup.py install

# Run InTeXration
python3 -m intexration