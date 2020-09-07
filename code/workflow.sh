#!/bin/bash

echo -e "\n$(date)"

# Source the conda environment
CONDA_BASE="$(conda info --base)"
CONDA_ENV="plain37"
source "$CONDA_BASE/etc/profile.d/conda.sh"
conda activate  "$CONDA_ENV"


set -euo pipefail


# Cmd below gets the directory where the script is located irrespective
# of where it's called from (won't work if last component of path is symlink)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# Download latest dataset
/bin/bash ./download_mirror.sh

DATA_DIR=../tmp.*
FILENAME="datos_abiertos_$(date -d "yesterday" +"%Y%m%d").zip"

# Run python scripts and commit changes
if [ -f  $DATA_DIR/$FILENAME ]; then
    echo -e "Running Python script\n"
    python parse_main_dataset.py $DATA_DIR/$FILENAME
    python update_daily_totals.py ; echo

    rm -rf $DATA_DIR
    git add ../data/covid19_mex_* ; git add ../data/daily_totals/covid19_mex_*
    git commit -m "Automatic update"
    git push #-f fork
else
    echo "ERROR: file not found"
fi


# end of script
