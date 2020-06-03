# EDGE device simulator (via docker-in-docker)

```bash
export DOCKER_HOST='127.0.0.1:22375'
docker-compose -f docker-compose.edge.yml up -d --scale device-http=4
```
