# gtfs-realtime-tools

A set of utilities for interacting with GTFS-realtime feeds.

## Set up

-	Install Python 3 and pip3 (`sudo apt install python3-pip`).

-	Install the protobuf compiler (also can be [downloaded
	here](https://developers.google.com/protocol-buffers/docs/downloads)):

	```
	sudo apt install protobuf-compiler
	```

	I think `brew install protobuf` might work on Mac.

	Run `protoc --version` to confirm that version 3 or higher is installed.

-	Install the protobuf Python library:

	```
	sudo pip3 install protobuf
	```

## Building

Run the build script:

```
./build.py
```

## Tools

-	**`gtfsrt2text.sh`**: Renders a GTFS-RT feed file in a human-readable text
	format for debugging.
-	**`get_timestamp.py`**: Extracts the timestamp field of a GTFS-RT feed file.
-	**`format_timestamp.py`**: Converts a POSIX timestamp (like the output of
	`get_timestamp.py`) to a human-readable format.
