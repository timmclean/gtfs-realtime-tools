#!/bin/bash
set -o errexit -o nounset -o pipefail

usage() {
	echo "Usage:"
	echo "  $0 <gtfsrt-feed-file>"
	echo "or:"
	echo "  cat <gtfsrt-feed-file> | $0"
	echo
	echo "Converts a GTFS-RT feed message into a human-readable text format for debugging."
	echo "Unfortunately, this text format is not easy to parse..."
	exit 1
}

if [ $# -eq 0 ]; then
	protoc --decode=transit_realtime.FeedMessage gtfs-realtime.proto
elif [ $# -eq 1 ]; then
	if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
		usage
	else
		cat "$1" | protoc --decode=transit_realtime.FeedMessage gtfs-realtime.proto
	fi
else
	usage
fi
