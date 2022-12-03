### Introduction

OCR images from a IIIF manifest to generate a git patch for [Miiify](https://github.com/nationalarchives/miiify).

### Example (requires Docker)

```bash
./boriiis.sh --name tesseract --creator john@nationalarchives.gov.uk --manifest https://miiifystore.s3.eu-west-2.amazonaws.com/iiif/ocrtest.json
```

Patching the [annotation repository](https://github.com/jptmoore/annotations) produces https://projectmirador.org/embed/?iiif-content=https://miiify.rocks/manifest/tesseract

### Status

Work in progress
