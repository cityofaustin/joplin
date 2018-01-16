# Joplin - CMS for the City of Austin

This is where you'll find the CMS for the City of Austin and atx.gov

## Background

bla bla bla

## Run locally

Make sure you have docker installed, then run:

```
./scripts/serve-local.sh
```

**NOTE** Fixture data is automatically loaded the first time you run the server. Add `LOAD_DATA=on` if you ever need to start with a fresh copy.

```
LOAD_DATA=on ./scripts/serve-local.sh
```

#### Access the admin

You can access the admin at `localhost:8000/admin` with the credentials `admin@austintexas.io`/`x`

#### Access the API

You can access the API at `localhost:8000/api`. You can see e.g. service pages by visiting `http://localhost:8000/api/pages/?format=json&type=base.ServicePage&fields=content,extra_content,topic(text),contacts(contact(name,email,phone,hours,location(name,street,city,state,zip,country)))`.


## Create migrations

While the server is running, run the following commands:

```
docker exec --interactive --tty joplin python joplin/manage.py makemigrations
docker exec --interactive --tty joplin python joplin/manage.py migrate
```

## Dump fixture data

Run the following to dump the latest page data. You might need to add other items from `base` or another package if you want other page types or snippets dumped.

#### To export new content

To export data changed in the CMS, run the following command:

```
docker exec --interactive --tty joplin python joplin/manage.py dumpdata --indent 2 --natural-primary --natural-foreign base wagtailcore.Page wagtailcore.PageRevision > fixtures/pages.json
```

#### To export internal data

After you add or change a model, you might also need to export the internal CMS data. Run the above command to export content data. Then run:

```
docker exec --interactive --tty joplin python joplin/manage.py dumpdata --indent 2 --natural-foreign wagtailcore.site wagtailcore.collection wagtailcore.grouppagepermission wagtailcore.groupcollectionpermission contenttypes auth.group > fixtures/base.json
```

## Create new app

```
APP_NAME=app_name_goes_here
docker exec joplin /bin/bash -c "mkdir -p \"$APP_NAME\" && cd joplin && python manage.py startapp \"$APP_NAME\""
```
