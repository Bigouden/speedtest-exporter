#!/usr/bin/env python3
# coding: utf-8
# pyright: reportMissingImports=false, reportGeneralTypeIssues=false

"""Speedtest Exporter"""

import logging
import os
import sys
import threading
from collections import defaultdict
from datetime import datetime
from json import loads
from json.decoder import JSONDecodeError
from subprocess import STDOUT, CalledProcessError, check_output  # nosec B404
from time import sleep
from typing import Callable
from wsgiref.simple_server import make_server

import pytz
import requests
from prometheus_client import PLATFORM_COLLECTOR, PROCESS_COLLECTOR
from prometheus_client.core import REGISTRY, CollectorRegistry, Metric
from prometheus_client.exposition import _bake_output, _SilentHandler, parse_qs

# Exporter Name Definition
SPEEDTEST_EXPORTER_NAME = os.environ.get(
    "SPEEDTEST_EXPORTER_NAME", "speedtest-exporter"
)

# Exporter Log Level Definition
SPEEDTEST_EXPORTER_LOGLEVEL = os.environ.get(
    "SPEEDTEST_EXPORTER_LOGLEVEL", "INFO"
).upper()
SPEEDTEST_EXPORTER_TZ = os.environ.get("TZ", "Europe/Paris")


def make_wsgi_app(
    registry: CollectorRegistry = REGISTRY, disable_compression: bool = False
) -> Callable:
    """Create a WSGI app which serves the metrics from a registry."""

    def prometheus_app(environ, start_response):
        # Prepare parameters
        accept_header = environ.get("HTTP_ACCEPT")
        accept_encoding_header = environ.get("HTTP_ACCEPT_ENCODING")
        params = parse_qs(environ.get("QUERY_STRING", ""))
        headers = [
            ("Server", ""),
            ("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0"),
            ("Pragma", "no-cache"),
            ("Expires", "0"),
            ("X-Content-Type-Options", "nosniff"),
        ]
        if environ["PATH_INFO"] == "/":
            status = "301 Moved Permanently"
            headers.append(("Location", "/metrics"))
            output = b""
        elif environ["PATH_INFO"] == "/favicon.ico":
            status = "200 OK"
            output = b""
        elif environ["PATH_INFO"] == "/metrics":
            status, tmp_headers, output = _bake_output(
                registry,
                accept_header,
                accept_encoding_header,
                params,
                disable_compression,
            )
            headers += tmp_headers
        else:
            status = "404 Not Found"
            output = b""
        start_response(status, headers)
        return [output]

    return prometheus_app


def start_wsgi_server(
    port: int,
    addr: str = "0.0.0.0",  # nosec B104
    registry: CollectorRegistry = REGISTRY,
) -> None:
    """Starts a WSGI server for prometheus metrics as a daemon thread."""
    app = make_wsgi_app(registry)
    httpd = make_server(addr, port, app, handler_class=_SilentHandler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()


start_http_server = start_wsgi_server

# Logging Configuration
try:
    pytz.timezone(SPEEDTEST_EXPORTER_TZ)
    logging.Formatter.converter = lambda *args: datetime.now(
        tz=pytz.timezone(SPEEDTEST_EXPORTER_TZ)
    ).timetuple()
    logging.basicConfig(
        stream=sys.stdout,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
        level=SPEEDTEST_EXPORTER_LOGLEVEL,
    )
except pytz.exceptions.UnknownTimeZoneError:
    logging.Formatter.converter = lambda *args: datetime.now(
        tz=pytz.timezone("Europe/Paris")
    ).timetuple()
    logging.basicConfig(
        stream=sys.stdout,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
        level="INFO",
    )
    logging.error("TZ invalid : %s !", SPEEDTEST_EXPORTER_TZ)
    os._exit(1)
except ValueError:
    logging.basicConfig(
        stream=sys.stdout,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
        level="INFO",
    )
    logging.error("SPEEDTEST_EXPORTER_LOGLEVEL invalid !")
    os._exit(1)

# Exporter Port Check
try:
    SPEEDTEST_EXPORTER_PORT = int(os.environ.get("SPEEDTEST_EXPORTER_PORT", "8123"))
except ValueError:
    logging.error("SPEEDTEST_EXPORTER_PORT must be int !")
    os._exit(1)

# Metrics Definition
METRICS = [
    {
        "name": "ping_jitter",
        "description": "Speedtest Ping Jitter in ms.",
        "type": "gauge",
    },
    {
        "name": "ping_latency",
        "description": "Speedtest Ping Latency in ms.",
        "type": "gauge",
    },
    {
        "name": "ping_low",
        "description": "Speedtest Ping Low in ms.",
        "type": "gauge",
    },
    {
        "name": "ping_high",
        "description": "Speedtest Ping High in ms.",
        "type": "gauge",
    },
    {
        "name": "download_bandwidth",
        "description": "Speedtest Download Bandwidth in bytes per second (B/s).",
        "type": "gauge",
    },
    {
        "name": "download_bytes",
        "description": "Speedtest Download Bytes in bytes.",
        "type": "gauge",
    },
    {
        "name": "download_elapsed",
        "description": "Speedtest Download Elapsed in ms.",
        "type": "gauge",
    },
    {
        "name": "download_latency_iqm",
        "description": "Speedtest Download IQM Latency in ms.",
        "type": "gauge",
    },
    {
        "name": "download_latency_low",
        "description": "Speedtest Download Low Latency in ms.",
        "type": "gauge",
    },
    {
        "name": "download_latency_high",
        "description": "Speedtest Download High Latency in ms.",
        "type": "gauge",
    },
    {
        "name": "download_latency_jitter",
        "description": "Speedtest Download Jitter Latency in ms.",
        "type": "gauge",
    },
    {
        "name": "upload_bandwidth",
        "description": "Speedtest Upload Bandwidth in bytes per second (B/s).",
        "type": "gauge",
    },
    {
        "name": "upload_bytes",
        "description": "Speedtest Upload Bytes in bytes.",
        "type": "gauge",
    },
    {
        "name": "upload_elapsed",
        "description": "Speedtest Upload Elapsed in ms.",
        "type": "gauge",
    },
    {
        "name": "upload_latency_iqm",
        "description": "Speedtest Upload IQM Latency in ms.",
        "type": "gauge",
    },
    {
        "name": "upload_latency_low",
        "description": "Speedtest Upload Low Latency in ms.",
        "type": "gauge",
    },
    {
        "name": "upload_latency_high",
        "description": "Speedtest Upload High Latency in ms.",
        "type": "gauge",
    },
    {
        "name": "upload_latency_jitter",
        "description": "Speedtest Upload Jitter Latency in ms.",
        "type": "gauge",
    },
    {
        "name": "packet_loss",
        "description": "Speedtest Percentage of Packet Loss during test.",
        "type": "gauge",
    },
]

# REGISTRY Configuration
REGISTRY.unregister(PROCESS_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
REGISTRY.unregister(REGISTRY._names_to_collectors["python_gc_objects_collected_total"])


# Speedtest Class
class SpeedtestCollector:
    """Speedtest Collector Class"""

    def __init__(self):
        pass

    @staticmethod
    def _get_speedtest_server():
        """Get Speedtest Server"""
        try:
            speedtest_cmd = check_output(  # nosec B603
                ["/usr/local/bin/speedtest", "-L", "-f", "json"],
                stderr=STDOUT,
                text=True,
            )
            servers = loads(speedtest_cmd.splitlines()[-1])["servers"]
            logging.debug(servers)
            for server in servers:
                if server["port"] == "443":
                    scheme = "https"
                else:
                    scheme = "http"
                res = requests.get(
                    f"{scheme}://{server['host']}:{server['port']}",
                    timeout=2,  # nosemgrep
                )
                if res.status_code == 200:
                    logging.debug(
                        "Server ID: %s (name: %s, host: %s, "
                        "port: %s, location: %s, country: %s)",
                        server["id"],
                        server["name"],
                        server["host"],
                        server["port"],
                        server["location"],
                        server["country"],
                    )
                    return server["id"]
                logging.error("Unable to connect to Server ID: %s", server["id"])
            logging.debug("None Speedtest Servers Found ! Exiting ...")
            os._exit(1)
        except CalledProcessError as exception:
            logging.error(loads(exception.output)["message"])
            os._exit(1)
        except JSONDecodeError as exception:
            logging.error(exception)
            os._exit(1)

    def run_speedtest(self):
        """Run Speedtest & Return JSON Results or Exit"""
        try:
            speedtest_cmd = check_output(  # nosec B603
                [
                    "/usr/local/bin/speedtest",
                    "--accept-license",
                    "--accept-gdpr",
                    "-s",
                    str(self._get_speedtest_server()),
                    "-f",
                    "json",
                ],
                stderr=STDOUT,
                text=True,
            )
            res = speedtest_cmd.splitlines()[-1]
            logging.debug(res)
            return loads(res)
        except CalledProcessError as exception:
            logging.error(loads(exception.output)["message"])
            os._exit(1)
        except JSONDecodeError as exception:
            logging.error(exception)
            os._exit(1)

    @staticmethod
    def _parse_results(res):
        labels = defaultdict(dict)
        datas = defaultdict(dict)
        try:
            labels["isp"] = res["isp"]
            labels["interface_name"] = res["interface"]["name"]
            labels["interface_internal_ip"] = res["interface"]["internalIp"]
            labels["interface_external_ip"] = res["interface"]["externalIp"]
            labels["interface_mac_address"] = res["interface"]["macAddr"]
            labels["interface_is_vpn"] = str(res["interface"]["isVpn"])
            labels["server_id"] = str(res["server"]["id"])
            labels["server_host"] = res["server"]["host"]
            labels["server_port"] = str(res["server"]["port"])
            labels["server_name"] = res["server"]["name"]
            labels["server_location"] = res["server"]["location"]
            labels["server_country"] = res["server"]["country"]
            labels["server_ip"] = res["server"]["ip"]
            labels["result_id"] = res["result"]["id"]
            labels["result_url"] = res["result"]["url"]
            labels["result_persisted"] = str(res["result"]["persisted"])
            datas["ping_jitter"] = res["ping"]["jitter"]
            datas["ping_latency"] = res["ping"]["latency"]
            datas["ping_low"] = res["ping"]["low"]
            datas["ping_high"] = res["ping"]["high"]
            datas["download_bandwidth"] = res["download"]["bandwidth"]
            datas["download_bytes"] = res["download"]["bytes"]
            datas["download_elapsed"] = res["download"]["elapsed"]
            datas["download_latency_iqm"] = res["download"]["latency"]["iqm"]
            datas["download_latency_low"] = res["download"]["latency"]["low"]
            datas["download_latency_high"] = res["download"]["latency"]["high"]
            datas["download_latency_jitter"] = res["download"]["latency"]["jitter"]
            datas["upload_bandwidth"] = res["upload"]["bandwidth"]
            datas["upload_bytes"] = res["upload"]["bytes"]
            datas["upload_elapsed"] = res["upload"]["elapsed"]
            datas["upload_latency_iqm"] = res["upload"]["latency"]["iqm"]
            datas["upload_latency_low"] = res["upload"]["latency"]["low"]
            datas["upload_latency_high"] = res["upload"]["latency"]["high"]
            datas["upload_latency_jitter"] = res["upload"]["latency"]["jitter"]
            datas["packet_loss"] = res["packetLoss"]
        except KeyError:
            pass
        return labels, datas

    def collect(self):
        """Collect & Return Prometheus Metrics"""
        # Get Labels & Datas
        labels, datas = self._parse_results(self.run_speedtest())
        logging.info("Labels : %s.", dict(labels))
        logging.info("Datas : %s.", dict(datas))
        # Forge Prometheus Metrics
        metrics = []
        for key, value in datas.items():
            if key in labels.keys():
                continue
            description = [i["description"] for i in METRICS if key == i["name"]][0]
            metric_type = [i["type"] for i in METRICS if key == i["name"]][0]
            metrics.append(
                {
                    "name": f"speedtest_{key.lower()}",
                    "value": float(value),
                    "description": description,
                    "type": metric_type,
                }
            )
        # Return Prometheurs Metrics
        for metric in metrics:
            prometheus_metric = Metric(
                metric["name"], metric["description"], metric["type"]
            )
            prometheus_metric.add_sample(
                metric["name"], value=metric["value"], labels=labels
            )
            yield prometheus_metric


# Main Function
def main():
    """Main Function"""
    logging.info("Starting Speedtest Exporter on port %s.", SPEEDTEST_EXPORTER_PORT)
    logging.debug("SPEEDTEST_EXPORTER_PORT: %s.", SPEEDTEST_EXPORTER_PORT)
    logging.debug("SPEEDTEST_EXPORTER_NAME: %s.", SPEEDTEST_EXPORTER_NAME)
    # Start Prometheus HTTP Server
    start_http_server(SPEEDTEST_EXPORTER_PORT)
    # Init SpeedtestExporterCollector
    REGISTRY.register(SpeedtestCollector())
    # Loop Infinity
    while True:
        sleep(1)


# Start
if __name__ == "__main__":
    main()
