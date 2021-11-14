FROM python:3-alpine

WORKDIR /app

COPY ./* /app/

RUN apk add build-base linux-headers && \
    pip install -r requirements.txt && \
    apk del build-base linux-headers

CMD python hermes-respeaker-pixel-ring.py
