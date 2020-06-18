FROM python:3.8-alpine AS builder
RUN apk update && apk add gcc musl-dev postgresql-dev \
        && pip install psycopg2-binary

# ---

FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE "bite.settings"

RUN apk update && apk add --no-cache postgresql-libs \
        && wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-alpine-linux-amd64-v0.6.1.tar.gz -qO- \
        | tar -xz -C /usr/local/bin
COPY --from=builder /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --chown=1000:1000 bite /srv/app/bite
COPY --chown=1000:1000 requirements.txt /tmp/requirements.txt

RUN mkdir -p /srv/appdata/bite/static \
        && chown -R 1000:1000 /srv/appdata/bite \
        && pip3 install -r /tmp/requirements.txt \
        && rm /tmp/requirements.txt

USER 1000:1000
WORKDIR /srv/app/bite
EXPOSE 8000/tcp
CMD ["python3", "manage.py", "runserver"]
