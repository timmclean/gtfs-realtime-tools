#!/bin/bash
set -o errexit -o nounset -o pipefail

# Where to store the data
# $data_dir must contain two directories: vehicle-positions and trip-updates
data_dir=$HOME/grt

pos_dir=$data_dir/vehicle-positions
trip_dir=$data_dir/trip-updates
timestamp=$(date '+%Y%m%d-%H%M%S-%N')

curl -s 'http://192.237.29.212:8080/gtfsrealtime/VehiclePositions' > ${pos_dir}/$timestamp
curl -s 'http://192.237.29.212:8080/gtfsrealtime/TripUpdates' > ${trip_dir}/$timestamp
