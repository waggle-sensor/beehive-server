#!/bin/sh
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

# will be done on beehive
../bin/filter-view plenario < recent.csv | ../bin/filter-sensors climate.csv > plenario.csv

# may be done on beehive or by consumer
../bin/prepare-for-plenario plenario < plenario.csv
