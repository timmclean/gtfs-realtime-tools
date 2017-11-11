#!/usr/bin/env python3

import datetime
import io
import os
import sys

from binascii import hexlify
from glob import glob
from shutil import copyfile, rmtree
from subprocess import check_call

from get_timestamp import get_timestamp
from gtfs_realtime_pb2 import FeedMessage

def run():
    if len(sys.argv) != 4:
        print("Usage:")
        print("  {} <input-dir> <output-dir> <date-to-extract>".format(sys.argv[0]))
        print()
        print("Extracts GTFS-RT data from the specified date into a separate archive,")
        print("while removing duplicate entries.")
        print("The input directory should contain archives from the GTFS-RT recorder script.")
        print()
        print("input-dir can be equal to output-dir.")
        print()
        print("Date must be in YYYY-MM-DD format.")
        return 1

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    date_to_extract = parse_date(sys.argv[3])

    dedupe_archives(input_dir, output_dir, date_to_extract)

def dedupe_archives(input_dir, output_dir, date_to_extract):
    # Check ahead of time if the output archive already exists
    output_archive_name = 'vehicle-positions-deduped-archive-{}.tar.bz2'.format(
        date_to_extract.strftime('%Y%m%d')
    )
    output_archive_file = os.path.join(output_dir, output_archive_name)
    if os.path.exists(output_archive_file):
        raise Exception('output file already exists at ' + output_archive_file)

    # Create directories for temporary work
    tmp_dir = os.path.join(output_dir, hexlify(os.urandom(16)).decode())
    os.mkdir(tmp_dir)
    raw_messages_dir = os.path.join(tmp_dir, 'raw_messages')
    os.mkdir(raw_messages_dir)
    processed_messages_dir = os.path.join(tmp_dir, 'processed_messages')
    os.mkdir(processed_messages_dir)

    # Extract feed messages from archives on date and date+1
    # (because archives can't reliably occur exactly on midnight,
    # and if they did, that might interfere with deduplication)
    check_call([
        'tar', 'xfz',
        find_archive_from_date(input_dir, date_to_extract)
    ], cwd=raw_messages_dir)
    check_call([
        'tar', 'xfz',
        find_archive_from_date(input_dir, date_to_extract + datetime.timedelta(days=1))
    ], cwd=raw_messages_dir)

    # Process messages
    for raw_message_file_name in os.listdir(raw_messages_dir):
        raw_message_file = os.path.join(raw_messages_dir, raw_message_file_name)

        # Check if timestamp is for the date we want
        ts = get_timestamp(raw_message_file)
        if ts is None or ts.date() != date_to_extract:
            # We don't care about this feed message, so skip
            continue

        formatted_ts = ts.strftime('%Y%m%d-%H%M%S')
        processed_message_file = os.path.join(processed_messages_dir, formatted_ts)

        # Have we already processed a message with this timestamp?
        if os.path.isfile(processed_message_file):
            # TODO check if they match?
            continue

        # Copy from raw to processed, and rename to use GTFS-RT timestamp
        copyfile(raw_message_file, processed_message_file)

    # Create output archive
    check_call(
        ['tar', 'cfj', output_archive_file] + os.listdir(processed_messages_dir),
        cwd=processed_messages_dir
    )

    # Clean up temp dir
    rmtree(tmp_dir)

    return 0

# Why is this not in stdlib???
def parse_date(date_str):
    if len(date_str) != 10 or date_str[4] != '-' or date_str[7] != '-':
        raise ValueError("invalid date: " + date_str)

    date_parts = date_str.split('-')
    return datetime.date(
        int(date_parts[0]), int(date_parts[1]), int(date_parts[2])
    )

def find_archive_from_date(dir_path, archive_date):
    paths_found = glob(os.path.join(
        dir_path,
        'vehicle-positions-archive-{:4d}{:02d}{:02d}-0?????-?????????.tar.gz'
        .format(archive_date.year, archive_date.month, archive_date.day)
    ))

    if len(paths_found) < 1:
        raise Exception("missing archive from required date: " + archive_date.isoformat())

    if len(paths_found) > 1:
        raise Exception('found more than one feed archive for ' + archive_date.isoformat())

    return paths_found[0]

if __name__ == '__main__':
    sys.exit(run())
