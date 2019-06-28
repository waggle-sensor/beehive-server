basedir=$(pwd $(dirname $_))

# # use venv python
source "$basedir/waggle-python/bin/activate"

# # add waggle tools
export PATH=$PATH:"$basedir/beehive-server/data-exporter":"$basedir/beehive-server/publishing-tools/bin"

# # set standard data paths
export DATASETS_DIR=/storage/datasets
export DATASETS_DIR_V2=/storage/datasets-v2
export DIGESTS_DIR=/storage/digests
export PROJECTS_DIR="$basedir/beehive-server/publishing-tools/projects"
