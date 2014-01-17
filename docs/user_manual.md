# User's Manual

## Installation

Please consult the [installation
guide](https://github.com/JDevlieghere/InTeXration/blob/master/docs/install.md)
for information on how to install InTeXration.

## Adding an API key

API keys are stored in a text file named `api_keys.txt` inside the `config`
directory. Each line contains exactly one key. Please note that leading or
trailing whitespaces are **not** allowed.

Using GUID's as API keys is recommended. You can generate those
[here](http://www.guidgenerator.com/).

Here's an example of the `api_keys.txt`:

```
0f304a9a-997a-4207-a1bf-3c74a009f5a0
787d8249-36bf-49cb-848b-a24c331881a2
e1271300-0247-4cdc-92ee-b6beec6a497d
```

Adding a key does not require the server to restart. You can add keys add run-
time.

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
http://server.com:8000/hook/0f304a9a-997a-4207-a1bf-3c74a009f5a0
```

Once your WebHook URL is created, add it to your repository. Navigate to the
settings page of your repository, find the *Service Hooks* page and add the URL
as a *WebHook URL*.

## .intexration
InTeXration uses the `.intexration` file from the root of your repository to
build en compile latex files. This file is basically and `ini`-file and should
look like this.

```ini
[file]
idx=index
bib=bibfile
```

The name of the section indicates the name of the `.tex`-file you want to
compile. We'll call this the *document name* from now on. The `idx` and `bib` key are both optional. If absent, InTeXration
assumes they have the same name as their parent file. Please note that no
extensions are used.

For each file that needs to be compiled, add an entry to this file.

Here's an example `.intexration` file:

```ini
[main]

[book]
bib=main

[print]
```

## URLs
InTeXration generates a URL for each document defined in the `.intexration`
file. One for the PDF and one for a HTML page showing the compilation log.

URL to download the PDF:
```
http://[host]:[port]/out/[repository name]]/[document name]
```

URL with build logs:
```
http://[host]:[port]/log/[repository name]]/[document name]
```

For example, using `server.com` as host, `8000` as port, `repo` as repository name and `main` as document
name, the URLs become:
```
http://server.com:8000/out/repo/main
http://server.com:8000/log/repo/main
```

These URLs can be included as links in your README.md to allow interested
parties to view the PDF rather than having to clone your repository and compile
the files inside it.