# QIWI Test Task
Simple test task for event and person and coupon!
 Written in [Aiohttp](https://docs.aiohttp.org/en/stable/)

## Getting Started

*Dependencies*:

1. Docker v19.03.5
1. Docker-Compose v1.24.1

Start.
```sh
$ make start
```

## Running tests

Pytest is used for writing and running the tests. As the project is running inside a docker container, tests should be run from the container:

```sh
$ make test
```
