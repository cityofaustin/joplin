build_artifacts contains

- requirements.txt
  A requirements.txt file created from our Pipfile. This is used to install our pip dependencies within a Docker container without needing to run pipenv within Docker. We don't commit requirements.txt so that our Pipfile remains our single source of truth.
