#!/bin/bash
set -o errexit -o nounset -o pipefail

# Where to store the data
# $data_dir must contain a directory called `vehicle-positions`
data_dir=$HOME/grt

pos_dir=$data_dir/vehicle-positions
timestamp=$(date '+%Y%m%d-%H%M%S-%N')

curl -s 'http://192.237.29.212:8080/gtfsrealtime/VehiclePositions' > ${pos_dir}/$timestamp
