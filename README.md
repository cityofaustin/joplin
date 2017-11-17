# Joplin - CMS for the City of Austin

This is where you'll find the CMS for the City of Austin and atx.gov

## Background

bla bla bla

## Run locally

Make sure you have docker installed, then run:

```
./scripts/serve-local.sh
```

The first time you start the server, you'll also need to do some setup. While the server is running, open a new terminal window and run:

```
./scripts/initial-setup.sh
```


## Create migrations

While the server is running, run the following commands:

```
docker exec joplin python joplin/manage.py makemigrations
docker exec joplin python joplin/manage.py migrate
```
