#!/usr/bin/env python3

import io
import sys
import tarfile

from gtfs_realtime_pb2 import FeedMessage

def run():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  {} <feed-archive-1> <feed-archive-2> ... <dest-archive>".format(sys.argv[0]))
        print()
        print("Combines the specified feed archives into one while removing duplicate entries.")
        print("All archives should be .tar.gz files.")
        return 1

    feed_archive_files = sys.argv[1:-1]
    dest_archive_file = sys.argv[-1]

    print("Extracting all feed messages from all tarfiles...")
    feed_messages = []
    for feed_archive_file in feed_archive_files:
        with tarfile.open(feed_archive_file) as feed_archive:
            members = feed_archive.getmembers()
            for member in members:
                if not member.isreg():
                    print("Found non-regular file in feed archive: {}".format(repr(feed_archive_file)))

                feed_messages.append(feed_archive.extractfile(member).read())

    print("Removing duplicates...")
    feed_messages_by_time = {}
    for (feed_message_idx, feed_message) in enumerate(feed_messages):
        if feed_message_idx % 1000 == 0 and feed_message_idx > 0:
            print(" Processed {}/{}.".format(feed_message_idx, len(feed_messages)))

        feed_message_parsed = FeedMessage.FromString(feed_message)
        timestamp = feed_message_parsed.header.timestamp

        # If we've already processed a feed msg with this timestamp
        if timestamp in feed_messages_by_time:
            # If this other feed msg does not exactly match the current one
            if feed_messages_by_time[timestamp] != feed_message:
                raise ValueError("found feed messages from same timestamp that do not match")

            # Otherwise, all good! We can skip this duplicate
        else:
            # Haven't seen this one before, so add it
            feed_messages_by_time[timestamp] = feed_message

    print(" Processed {}/{} (removed {} duplicates).".format(
        len(feed_messages), len(feed_messages),
        len(feed_messages) - len(feed_messages_by_time)
    ))

    print("Writing output tarfile...")
    with tarfile.open(dest_archive_file, 'w:gz') as dest_archive:
        for (timestamp, feed_message) in feed_messages_by_time.items():
            entry_header = tarfile.TarInfo(str(timestamp))
            entry_header.size = len(feed_message)
            dest_archive.addfile(entry_header, io.BytesIO(feed_message))

    return 0

if __name__ == '__main__':
    sys.exit(run())
