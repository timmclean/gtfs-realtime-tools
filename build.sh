#!/bin/bash
set -o errexit -o nounset -o pipefail

# Generate GTFS-RT [de]serialization code
# Note: requires the Protocol Buffer compiler from Google
protoc --python_out deduplicator gtfs-realtime.proto
protoc --python_out misc gtfs-realtime.proto
