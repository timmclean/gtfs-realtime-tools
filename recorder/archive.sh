#!/bin/bash
set -o errexit -o nounset -o pipefail

data_dir=$HOME/grt

# Generate a new ID randomly to avoid collisions
new_id=$((cat /dev/urandom || true) | (tr -dc a-zA-Z0-9 || true) | head -c 20)

for feed_type in vehicle-positions; do
	# Get the current feed archive dir
	feed_archive_dir=$(readlink -f "${data_dir}/${feed_type}")

	# Atomically update feed archive link to point at new dir
	mkdir "${data_dir}/${feed_type}-${new_id}"
	ln -sfn "${feed_type}-${new_id}" "${data_dir}/${feed_type}"

	# Give any current downloads a chance to finish
	sleep 5

	# Clear out empty files (from failed polls)
	find "${feed_archive_dir}" -type f -size 0c -exec rm {} \;

	# Compress feed archive into tarball
	cd $feed_archive_dir
	timestamp=$(date '+%Y%m%d-%H%M%S-%N')
	tar cfz "${data_dir}/${feed_type}-archive-${timestamp}.tar.gz" *

	# Remove old feed archive dir
	rm -rf "${feed_archive_dir}"
done

# Run deduplicator
yesterday=$(date --date='yesterday' '+%Y-%m-%d')
"$data_dir/deduplicator/dedupe_archives.py" "$HOME/grt" "$HOME/grt/public" "$yesterday"
