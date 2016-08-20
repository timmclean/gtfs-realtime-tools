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

-	Install the protobuf Python library:

	```
	sudo pip3 install protobuf
	```

## Building

Run the build script:

```
./build.py
```
