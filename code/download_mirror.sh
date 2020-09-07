#!/bin/bash

set -euo pipefail

# The following mirror was set up for us to use
URL="https://repounam.org/data/.input"

# The unicode of the csv file has been fixed, however there has been a
# typo (either utf or uft) in the name of the file
PATTERN="$(date -d "yesterday" +"%Y-%m-%d")_u(tf|ft)8.zip"
ZIP_FILE="$(curl -sSL "$URL" | tac | tac | grep -Eo "$PATTERN" | head -1)"
echo -e "Matched zip file name is $ZIP_FILE\n"


# Cmd below gets the directory where the script is located irrespective
# of where it's called from (won't work if last component of path is symlink)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

FILENAME="datos_abiertos_$(date -d "yesterday" +"%Y%m%d").zip"


# Download zip file
if [ ! -z "$ZIP_FILE" ]; then
    echo "Page is updated; starting download"

    # Create temporary directory above the code directory
    TMP_DIR=$(mktemp -dp ..)
    echo -e "Temporary directory is $TMP_DIR\n"

    # We make sure that the tmp directory is deleted in case of error
    trap 'rm -rf "$TMP_DIR"' ERR
    #TODO: this doesn't seem to be working

    curl -L "$URL/$ZIP_FILE" -o "$TMP_DIR/$FILENAME"
    echo -e "\nDownload finished\n"
else
    echo  -e "ERROR: page is not updated"
    exit 1
fi

# end of script
