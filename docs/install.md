# Installation

## Prerequisites

InTeXration requires:

- Python 3
- pdflatex (part of TexX Live)
- pip

Use pip to install the Python package requirements.

```bash
pip install -r requirements.txt
```

Installing the full version of TeX Live is recommended. If you'll be running InTeXration on Ubuntu, [this repository](https://github.com/scottkosty/install-tl-ubuntu) might come in handy.

## Configuring

All configuration files are located in the `config` directory.

### Config
The `config.ini` file contains the server properties. Without this file InTeXration will not start.

This is an example of the configuration file:
```ini
[SERVER]
host=0.0.0.0
port=8000
```

### Logging
The `logging.ini` file defines the the logging formatter and handlers. Please consult the [Python 3 documentationn](http://docs.python.org/2/library/logging.config.html) when editing this file.

This is the default logger configuration file:
```ini
[formatters]
keys=default

[loggers]
keys=root

[formatter_default]
format=%(asctime)s:%(levelname)s:%(message)s
class=logging.Formatter

[handlers]
keys=error_file

[handler_error_file]
class=logging.FileHandler
level=WARNING
formatter=default
args=('logs/error.log', 'w')

[logger_root]
level=DEBUG
formatter=default
handlers=error_file
```
