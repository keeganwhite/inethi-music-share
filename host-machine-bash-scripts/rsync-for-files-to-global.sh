#!/bin/bash
set -a # automatically export all variables
source .env
set +a
rsync -rav --stats -e "ssh -i $PEM_FILE" $LOCAL_SYNC_FOLDER_PATH $GLOBAL_SYNC_FOLDER