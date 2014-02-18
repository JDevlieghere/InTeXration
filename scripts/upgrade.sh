#!/usr/bin/env bash

# Fetch latest version from git
git fetch --all
git checkout master

# Install new requirements
sudo pip3 install -r requirements.txt

# Install using setup.py
sudo python3 setup.py install
