# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# BITE - A Basic/IoT/Example
# Copyright (C) 2020-2021 Daniele Viganò <daniele@vigano.me>
#
# BITE is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BITE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

FROM python:3.9-alpine AS builder
RUN apk update && apk add gcc musl-dev postgresql-dev \
        && pip install psycopg2-binary

# ---

FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE "bite.settings"

RUN apk update && apk add --no-cache postgresql-libs \
        && wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-alpine-linux-amd64-v0.6.1.tar.gz -qO- \
        | tar -xz -C /usr/local/bin
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --chown=1000:1000 requirements.txt /srv/app/bite/requirements.txt
RUN pip3 install --no-cache-dir -r /srv/app/bite/requirements.txt

COPY --chown=1000:1000 bite /srv/app/bite
RUN python3 -m compileall -q /srv/app/bite \
        && mkdir -p /srv/appdata/bite/static \
        && chown -R 1000:1000 /srv/appdata/bite

USER 1000:1000
WORKDIR /srv/app/bite
EXPOSE 8000/tcp
CMD ["python3", "manage.py", "runserver"]
