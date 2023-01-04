SampleNote PyPI server
====================

This is the PyPI server of SampleNote

## How to add a new release with the make command?
You can use the following make command to create a new app release:
```bash
make bump app=samplenotedata version=0.1.0 protocol=ssh org=SampleNote repo=samplenote-data
```

## How to reference the libraries in `requirements.txt`?
Reference the package in your `requirements.txt` as follows:
```shell
--extra-index-url https://samplenote.github.io/python-package-server/
midi==0.3.0
...
```
