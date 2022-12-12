### Introduction

OCR from a IIIF manifest to generate a git patch for [Miiify](https://github.com/nationalarchives/miiify).


### Build the tool

```bash
docker build -t jptmoore/boriiis .
```

### Run the tool

```bash
./boriiis.sh --name my-collection --creator john --manifest https://miiifystore.s3.eu-west-2.amazonaws.com/iiif/ocrtest.json
```

Patching the [annotation repository](https://github.com/jptmoore/annotations) produces https://projectmirador.org/embed/?iiif-content=https://miiify.rocks/manifest/tesseract


### Usage

```
./boriiis.sh --help
Usage: main.py [OPTIONS]

Options:
  --name TEXT      [required]
  --manifest TEXT  [required]
  --lang TEXT
  --creator TEXT
  --oem INTEGER
  --psm INTEGER
  --preview        Output result of OCR only.
  --version        Show the version and exit.
  --help           Show this message and exit.
```

### Status

Work in progress
