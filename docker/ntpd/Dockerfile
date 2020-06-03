FROM alpine:3.9

RUN apk update && apk add chrony && \
    chown -R chrony:chrony /var/lib/chrony
COPY ./chrony.conf /etc/chrony/chrony.conf

EXPOSE 123/udp
ENTRYPOINT ["chronyd", "-d", "-s", "-x"]
