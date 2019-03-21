### How to Restore a Heroku backup onto your local Joplin Database.

1. Download a database backup from heroku.
2. Run:
    ```
    pg_restore --verbose --clean --no-acl --no-owner -h localhost -U joplin -d joplin
    /path/to/backup/file
    ```
3. Connect with:
    `psql postgres://joplin@localhost:5432/joplin`
