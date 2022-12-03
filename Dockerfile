FROM jptmoore/miiify as miiify

USER root

# python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# tesseract/git
RUN apk add --update --no-cache tesseract-ocr git

# boriiis deps
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps

COPY requirements.txt requirements.txt
COPY src .

RUN pip install -r requirements.txt

USER miiify

ENTRYPOINT ["python", "main.py"]
