# Persistent KV store service

## Dev guide

### Env setup

```bash
./one-time-setup.sh
```

### Create venv & install dependencies

```bash
just env
just install
```

### Start service locally

Note: default to use local storage. You can also test the service with other storage backends such as MinIO or S3, see `config.settings` to enable them.

```bash
just start
```

### Build service docker image

```bash
docker-compose build
```

### Start docker service

All services:

```bash
docker-compose up
```