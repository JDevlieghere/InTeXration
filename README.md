![InTeXration](http://cdn.jonasdevlieghere.com/intexration.png)

Features
--------
InTeXration is a *continuous integration* tool for building *LaTeX* documents. It integrates with GitHub using a WebHook. On each push latex files specified in the `.intexration` file are compiled to a PDF. A fixed URL to the resulting pdf and the corresponding build log can be added to the repository's README to provide an up to date, compiled version of the latex document(s) inside.

Screenshot
----------
![InTeXration Screenshot](http://cdn.jonasdevlieghere.com/intexration_screenshot.png)

Documentation
-------------
This project is in an early development phase. Documentation might be missing or lagging behind.

- [User's Manual](https://github.com/JDevlieghere/InTeXration/blob/master/docs/manual.md)
- [Installation](https://github.com/JDevlieghere/InTeXration/blob/master/docs/install.md)
- [Configuration](https://github.com/JDevlieghere/InTeXration/blob/master/docs/config.md)

Use InTeXration
---------------

If you would like to try out InTeXration but don't have access to a VPS or decicated server please contact me for an API key.
I'm running the latest stable release at [intexration.jonasdevlieghere.com:8000](http://intexration.jonasdevlieghere.com:8000).
API keys are currently not linked to a repositories so can be used for multiple projects.

![mail](http://cdn.jonasdevlieghere.com/mail.png)

License
-------
Apache License, Version 2.0 (See [LICENSE](https://github.com/JDevlieghere/InTeXration/blob/master/LICENSE))