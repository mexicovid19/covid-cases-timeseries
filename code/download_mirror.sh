#!/bin/bash

set -euo pipefail

# The following mirror was set up for us to use
URL="https://repounam.org/data/.input"
ZIP_FILE="$(date -d "yesterday" +"%Y-%m-%d"_utf8.zip)"
# The unicode of the csv file has been fixed


# Cmd below gets the directory where the script is located irrespective
# of where it's called from (won't work if last component of path is symlink)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

FILENAME="datos_abiertos_$(date -d "yesterday" +"%Y%m%d").zip"

# Create temporary directory above the code directory
TMP_DIR=$(mktemp -dp ..)
echo -e "Temporary directory is $TMP_DIR\n"

# We make sure that the tmp directory is deleted in case of error
trap 'rm -rf "$TMP_DIR"' ERR


# Download zip file
if curl -sSL "$URL" | tac | tac | grep -q "$ZIP_FILE"; then
    echo -e "Page is updated; starting download\n"
    curl -L "$URL/$ZIP_FILE" -o "$TMP_DIR/$FILENAME"
    echo -e "\nDownload finished\n"
else
    echo  -e "ERROR: page is not updated"
    exit 1
fi

# end of script
