#!/usr/bin/env python3

import sys

from datetime import datetime

def run():
    if len(sys.argv) not in [1, 2]:
        print("Usage:")
        print("  {} <seconds-since-epoch>".format(sys.argv[0]))
        print("or:")
        print("  echo <seconds-since-epoch> | {}".format(sys.argv[0]))
        print()
        print("<seconds-since-epoch> should be a POSIX timestamp.")
        return 1

    if len(sys.argv) == 2:
        timestamp = sys.argv[1]
    else:
        timestamp = int(sys.stdin.read().strip())

    print(datetime.fromtimestamp(timestamp).isoformat())
    return 0

if __name__ == '__main__':
    sys.exit(run())
