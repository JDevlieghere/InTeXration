# Configuration

- [Overview](#overview)
- [Server](#server)
- [Compilation](#compilation)
- [Configuration File](#configuration-file)

## Overview
There are two possible ways to configure InTeXration:

 - By using command line arguments to change individual settings. This is the preferred method to change a single setting.
 - By exporting the configuration file, editing it and importing it again. Settings can be transfered between different installs as long as the versions match.

## Server

The server is identified by a hostname and port. By default the hostname is `localhost` and the port `8000`. If you want to access the InTeXration server in your browser without specifying a port number, use port `80` which is the HTTTP default.

Setting the hostname to `localhost`:
```bash
python3 -m intexration config --host localhost
```

Setting the port to `8000`:
```bash
python3 -m intexration config --host 8000
```

## Compilation

Currently, compilation settings are not configurable using command line arguments. Please refer to the next section for an example.

You can specify the branch that will trigger compilation (lazy or not). The default `branch` is set to the `master` branch.

InTeXration supports lazy compilation: this means that the document will only be compiled when necessary. The first view will experience a delay proportional to the compilation time. When lazy compilation is disabled, the document will be compiled as soon as the server receives the request. The advantage of using lazy compilation is reducing server load, especially when users are pushing frequently to the selected branch. The `lazy` option is disabled by default.

When more than one file is provided for compilation InTeXration can run those in parallel. This means a significant performance increase. The `threaded` option is enabled by default.

## Configuration File
A default config file look like this:

```ini
[SERVER]
host=localhost
port=8000

[INTEXRATION]
output=/home/intexration/out
explore=yes

[COMPILATION]
branch=master
lazy=no
threaded=yes
```