FROM python:3.8-alpine AS builder
RUN apk update && apk add gcc musl-dev postgresql-dev \
        && pip install psycopg2-binary

# ---

FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE "freedcs.settings"

RUN apk update && apk add --no-cache postgresql-libs
COPY --from=builder /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --chown=1000:1000 freedcs /srv/app/freedcs
COPY --chown=1000:1000 requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt && rm /tmp/requirements.txt

USER 1000:1000
WORKDIR /srv/app/freedcs
EXPOSE 8000/tcp
CMD ["python3", "manage.py", "runserver"]
