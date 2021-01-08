#! /usr/bin/env bash
set -a # automatically export all variables
source .env
set +a
date=$(date +%Y%m%d)
for file in $TEMP_FILE_LOCATION_ALL ; do
    basename=${file%.*}    # Remove extension
    extension=${file##*.}  # Remove basename
    mv "$file" "$basename"_"$date.$extension"
    python $PYTHON_SCRIPT_LOCATION
done
mv $TEMP_FILE_LOCATION_ALL $LOCAL_SYNC_FOLDER_PATH
rsync  -rav --stats -e "ssh -i $PEM_FILE" $LOCAL_SYNC_FOLDER_PATH_ALL $GLOBAL_SYNC_FOLDER