#!/bin/bash
set -o errexit -o nounset -o pipefail

# Where to store the data
# $data_dir must contain a directory called `vehicle-positions`
data_dir=$HOME/grt

pos_dir=$data_dir/vehicle-positions
timestamp=$(date '+%Y%m%d-%H%M%S-%N')

curl -s 'https://webapps.regionofwaterloo.ca/api/grt-routes/api/vehiclepositions' > ${pos_dir}/$timestamp
