#!/usr/bin/env python3

import sys

from gtfs_realtime_pb2 import FeedMessage

def run():
    if len(sys.argv) != 2:
        print("Usage: {} <feed-msg-file>".format(sys.argv[0]))
        print()
        print("Extracts the timestamp field of the specified GTFS-RT feed file.")
        print("The output will be a POSIX timestamp.")
        return 1

    feed_msg_file = sys.argv[1]

    with open(feed_msg_file, 'rb') as f:
        feed_msg_raw = f.read()

    feed_msg = FeedMessage.FromString(feed_msg_raw)
    print(feed_msg.header.timestamp)

    return 0

if __name__ == '__main__':
    sys.exit(run())
