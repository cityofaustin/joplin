cat joplin/db/smuggler/pages.json | jq -r '.[].fields.file|select(.)' | while read line
do
  if [ -f media/$line ]; then
    echo media/$line already exists, skipping...
  else
    echo Downloading $line
    curl -# https://joplin-austin-gov.s3.amazonaws.com/media/$line -o media/$line
  fi
done