# use venv python
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
source /home/sean/waggle-python/bin/activate

# add waggle tools
export PATH=$PATH:/home/sean/beehive-server/data-exporter:/home/sean/beehive-server/publishing-tools/bin

# set standard data paths
export DATASETS_DIR=/storage/datasets
export DIGESTS_DIR=/storage/digests
export PROJECTS_DIR=/home/sean/beehive-server/publishing-tools/projects
