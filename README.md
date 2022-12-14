### Introduction

OCR from a IIIF v3 manifest to generate a git patch for [Miiify](https://github.com/nationalarchives/miiify).


### Build the tool

```bash
docker build -t jptmoore/boriiis .
```

### Run the tool

![](render.gif)

Patching the [annotation repository](https://github.com/jptmoore/annotations) produces https://projectmirador.org/embed/?iiif-content=https://miiify.rocks/manifest/tesseract


### Usage

```
./boriiis.sh --help
Usage: main.py [OPTIONS]

Options:
  --name TEXT           Name of collection.  [required]
  --manifest TEXT       IIIF manifest.  [required]
  --lang [eng|fra]      Current languages supported.  [default: eng]
  --creator TEXT        Creator of annotations.  [default:
                        john.moore@nationalarchives.gov.uk]
  --page-limit INTEGER  Server-side annotation pagination.  [default: 200]
  --oem INTEGER         Tesseract engine mode.  [default: 3]
  --psm INTEGER         Tesseract page segmentation mode.  [default: 3]
  --preview             Text output of OCR.
  --update              To add to existing data.
  --debug               Enable debug mode.
  --version             Show the version and exit.
  --help                Show this message and exit.
```

### Status

Work in progress
