# HTTPyMonitor

Simple HTTP forwarder and monitor with web GUI.

![HTTPyMonitor screenshot](doc/images/HTTPyMonitor-screenshot.png)

## Topology

```
                                +-----------------------+
                                |    HTTPyMonitor       |
     +-------------+            |  +-----------------+  |
     | WEB browser | <-----------> | webserver (GUI) |  |
     +-------------+            |  +-----------------+  |
                                |          ^            |
                                |          |            |
                                |          v            |
     +-------------+            |  +-----------------+  |                +-----------------+
     | HTTP client | <-----------> | HTTP forwarder  | <---------------> | HTTP server     |
     +-------------+            |  +-----------------+  |                +-----------------+
                                |                       |
                                |+---------------------+|
```

## Usage

```bash
docker run -d -p 8080:8080 -p 8081:8081 -e PROXY_DESTINATION=https://api.github.com --name httpymonitor-github-api smartondev/httpymonitor
```

This example:

- runs the HTTPyMonitor container in the background
- forwards incoming HTTP requests to `https://api.github.com`
- listens on port `8080` for web based GUI
- listens on port `8081` for incoming HTTP requests
- names the container `httpymonitor-github-api`

## Docker images versions

- `nightly`: `smartondev/httpymonitor:nightly` (latest)
- `x.y.z`: `smartondev/httpymonitor:x.y.z` (stable)
- `latest`: `smartondev/httpymonitor:latest` (latest stable)

## Author

[Márton Somogyi](https://github.com/kamarton)
