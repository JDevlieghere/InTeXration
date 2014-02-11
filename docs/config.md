# Configuration

- [Overview](#overview)
- [Global](#global)
- [Logging](#logging)

## Overview

The configuration file is located in `/home/intexration/config` and is named `config.cfg`. The default configuration file looks like this:

```ini
[SERVER]
host=localhost
port=8000

[DOCUMENTS]
explore=yes

[COMPILATION]
branch=master
lazy=no
threaded=yes
```

The logging configuration file is located in the same directory and is called `logging.cfg`. The default logging configuration file looks like this:

```ini
[formatters]
keys=default

[loggers]
keys=root

[formatter_default]
format=[%(asctime)s] [%(levelname)s] %(message)s
class=logging.Formatter

[handlers]
keys=stream, file

[handler_stream]
class=logging.StreamHandler
level=DEBUG
formatter=default
args=(sys.stdout,)

[handler_file]
class=logging.FileHandler
level=WARNING
formatter=default
args=(os.path.expanduser("~") + '/intexration.log', 'a')

[logger_root]
level=DEBUG
formatter=default
handlers=stream, file
```

Both are basically ini-files. If either of them does not exist, InTeXration will try to create a default one for you. This might fail due to a lack of permissions. Either create the files and folders yourself, or run InTeXration for the first time with root permissions.

## Global

### Server

The server is identified by a hostname and port. By default the hostname is `localhost` and the port `8000`. If you want to access the InTeXration server in your browser without specifying a port number, use port `80` which is the HTTTP default.

### Documents

InTeXration stores the compiled documents in a folder on disk. This folder is specified in the configuration file. Refer to the last section for more information on how to alter this file. The default location is `/home/intexration/out`, or a folder called `out` in the intexration user's home directory. Make sure that whatever folder you select, it exists and is writable by the InTeXration server.

The server keeps track of the files it has compiled since it started. Because this information is kept in memory, restarting the server causes it to forget about previously compiled documents. Use the `explore` option to enable the server to look on disk for existing compiled documents.

### Compilation

You can specify the branch that will trigger compilation (lazy or not). The default `branch` is set to the `master` branch.

InTeXration supports lazy compilation: this means that the document will only be compiled when necessary. The first view will experience a delay proportional to the compilation time. When lazy compilation is disabled, the document will be compiled as soon as the server receives the request. The advantage of using lazy compilation is reducing server load, especially when users are pushing frequently to the selected branch. The `lazy` option is disabled by default.

When more than one document is provided for compilation InTeXration can run the compilation process in parallel. This means a significant performance increase. The `threaded` option is enabled by default.

## Logging

The logging configuration file follows the specifications as described by the logging library that is part of the Python distribution. Please refer to its documentation for more info on how to configure your logging.