# User's Manual

## Installation

Please consult the [installation
guide](https://github.com/JDevlieghere/InTeXration/blob/master/docs/install.md)
for information on how to install InTeXration.

## Adding an API key

Using GUID's as API keys is recommended. You can generate those
[here](http://www.guidgenerator.com/).

Use the command line argument `-add` to authorize an API key:
```bash
python -m intexration -add 0F304A9A-997A-4207-A1BF-3C74A009F5A0
```

#### Listing

To list all API keys currently registered, use the `-list` argument.
```bash
python -m intexration -list
```
A list of keys will be printed to the standard output stream.

#### Removing

To remove an API key, simply use the `-remove` argument.
```bash
python -m intexration -remove 0F304A9A-997A-4207-A1BF-3C74A009F5A0
```


## WebHook

Once you have created an API key for your repository, you can create a WebHook
URL:

```
http://[host]:[port]]/hook/[api key]
```
Please note there is no trailing `/` which would invalidate the URL.

For example, using `server.com` as host, `8000` as port and the first API key
fromt he list above, the URL becomes:
```
http://server.com:8000/hook/0F304A9A-997A-4207-A1BF-3C74A009F5A0
```

Once your WebHook URL is created, add it to your repository. Navigate to the
settings page of your repository, find the *Service Hooks* page and add the URL
as a *WebHook URL*.

## .intexration
InTeXration uses the `.intexration` file from the root of your repository to
build en compile latex files. This file is basically and `ini`-file and  could
look like this.

```ini
[file]
dir=report
idx=index
bib=bibfile
```

The name of the section indicates the name of the `.tex`-file you want to
compile. We'll call this the *document name* from now on. There are 3 optional keys:

- **dir**: The directory in which the document is located.
- **idx**: The name of the index file.
- **bib**: The name of the BibTex file.


The `dir`, `idx` and `bib` key are all optional. If absent, InTeXration assumes that the document is located in the root of your repository and that the index an BibTex file have the same name as the document. Please note that no extensions are used.


For each file that needs to be compiled, add an entry to this file.

Here's an example `.intexration` file:

```ini
[main]

[book]
dir=alternative
bib=main

[print]
dir=alternative
```

## URLs
InTeXration generates a URL for each document defined in the `.intexration`
file. One for the PDF and one for a HTML page showing the compilation log.

URL to download the PDF:
```
http://[host]:[port]/pdf/[repository_owner]/[repository name]]/[document name]
```

URL with build logs:
```
http://[host]:[port]/log/[repository_owner]/[repository name]]/[document name]
```

For example, using `server.com` as host, `8000` as port, `repo` as repository
name, `owner` as repository owner and `main` as document name, the URLs become:
```
http://server.com:8000/pdf/owner/repo/main
http://server.com:8000/log/owner/repo/main
```

These URLs can be included as links in your README.md to allow interested
parties to view the PDF rather than having to clone your repository and compile
the files inside it.