#!/usr/bin/env bash

# Fetch latest version from git
git fetch --all
git checkout master

# Install using setup.py
python3 setup.py install