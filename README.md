## REST API / Web Service Stress Tester

This is a simple tool to stress test your REST API / Web Service.

It is written in Python and uses `aiohttp` to make asynchronous requests, along with `uvloop` to speed up the event loop. uvloop is optional, and is not included in the requirements, if you'd like to use it, be sure to install it via `pip install uvloop` (only currently supported on linux).

Use `python3 main.py -h` to see the help message and get started.

![Preview](https://i.imgur.com/GPJgCxJ.gif)
