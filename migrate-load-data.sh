echo "Running migrations..."
python ./joplin/manage.py migrate --noinput

echo "Migrating static files to S3 bucket ..."
python ./joplin/manage.py collectstatic --noinput
