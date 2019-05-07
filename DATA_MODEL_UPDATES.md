# Updating the Data Model

Get Joplin running, if it doesn't run and you get a module error, try removing the joplin docker image and running serve-local again.

* Verify we can log in at localhost:8000.

* Find joplin/base/models.py
* Find the model we're updating
* After updating the model, you should be able to run Joplin and it should notice it needs migrations

* Get into the shell in the joplin docker container
* Make migrations:
  * python joplin/manage.py makemigrations
  * Run migrations:
    * python joplin/manage.py migrate

Make sure everything still works.

# Updating backups
* Remove all docker containers related to Joplin
* Go back to a commit before any model changes.
* run serve-local (doesn't add users)
* run `scripts/serve-local.sh`
* Once you can log in to wagtail, go to localhost:8000/django-admin/load
* Load pages.json

---

* Shut down joplin
* Go back to a commit with data model changes and migrations
* Start up joplin serve-local
* go to localhost:8000/django-admin/dump
* Replace pages.json with what you just downloaded.
* Commit it.

---

* Go back to a commit before any model changes.
* run `scripts/serve-local.sh`
* Make sure you can log in to localhost:8000
* go to a commit with the model changes
* run serve-local
* get into the shell in the joplin container
* run python joplin/manage.py dbbackup
* Commit it.
