#!/usr/bin/env python3

import datetime
import os
import sys

from dedupe_archives import dedupe_archives, parse_date

def run():
    if len(sys.argv) != 5:
        print("Usage:")
        print("  {} <input-dir> <output-dir> <start-date> <end-date>".format(sys.argv[0]))
        print()
        print("Runs dedupe_archives.py for all dates between start-date and end-date (inclusive).")
        return 1

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    start_date = parse_date(sys.argv[3])
    end_date = parse_date(sys.argv[4])

    if start_date > end_date:
        raise ValueError('invalid date range: {} to {}'.format(start_date, end_date))

    date_to_extract = start_date
    while date_to_extract <= end_date:
        print("Processing " + date_to_extract.isoformat())
        dedupe_archives(input_dir, output_dir, date_to_extract)

        date_to_extract += datetime.timedelta(days=1)

    return 0

if __name__ == '__main__':
    sys.exit(run())
