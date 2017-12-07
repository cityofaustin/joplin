# Joplin - CMS for the City of Austin

This is where you'll find the CMS for the City of Austin and atx.gov

## Background

bla bla bla

## Run locally

Make sure you have docker installed, then run:

```
./scripts/serve-local.sh
```

**NOTE** The first time you start the server, you'll also need to do some setup. While the server is running, open a new terminal window and run:

```
./scripts/initial-setup.sh
```

#### Access the admin

You can access the admin at `localhost:800/admin` with the credentials `admin@austintexas.io`/`x`

#### Access the API

You can access the API at `localhost:8000/api`. You can see e.g. service pages by visiting `http://localhost:8000/api/pages/?format=json&type=base.ServicePage&fields=content,extra_content,theme(text)`.


## Create migrations

While the server is running, run the following commands:

```
docker exec joplin python joplin/manage.py makemigrations
docker exec joplin python joplin/manage.py migrate
```
