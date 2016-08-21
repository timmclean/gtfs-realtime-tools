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

decode() {
	protoc --decode=transit_realtime.FeedMessage --proto_path "$(dirname "$0")" "$(dirname "$0")/gtfs-realtime.proto"
}

if [ $# -eq 0 ]; then
	decode
elif [ $# -eq 1 ]; then
	if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
		usage
	else
		cat "$1" | decode
	fi
else
	usage
fi
