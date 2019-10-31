# The default behavior of Joplin is to point to the remote staging CMS_MEDIA location,
# which means you no longer need to download media files manually.
# Previously, that was something we needed to do with this script.
# It parsed a backup file from the db/smuggler directory and placed all referenced images into the local media folder.
# It is no longer required as part of the development process.

cat joplin/db/smuggler/pages.json | jq -r '.[].fields.file|select(.)' | while read line
do
  if [ -f media/$line ]; then
    echo media/$line already exists, skipping...
  else
    echo Downloading $line
    curl -# https://joplin-austin-gov.s3.amazonaws.com/media/$line -o media/$line
  fi
done
