#!/usr/bin/env python3

import sys

from gtfs_realtime_pb2 import FeedMessage

def get_timestamp(feed_msg_file_path):
    with open(feed_msg_file_path, 'rb') as f:
        feed_msg_raw = f.read()

    feed_msg = FeedMessage.FromString(feed_msg_raw)
    return feed_msg.header.timestamp

def run():
    if len(sys.argv) != 2:
        print("Usage: {} <feed-msg-file>".format(sys.argv[0]))
        print()
        print("Extracts the timestamp field of the specified GTFS-RT feed file.")
        print("The output will be a POSIX timestamp.")
        return 1

    feed_msg_file = sys.argv[1]

    print(get_timestamp(feed_msg_file))

    return 0

if __name__ == '__main__':
    sys.exit(run())
