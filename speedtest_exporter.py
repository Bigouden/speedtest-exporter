#!/usr/bin/env python3
#coding: utf-8

'''Speedtest Exporter'''

import logging
import os
import sys
import time
from collections import defaultdict
import speedtest
from prometheus_client.core import REGISTRY, Metric
from prometheus_client import start_http_server, PROCESS_COLLECTOR, PLATFORM_COLLECTOR

SPEEDTEST_EXPORTER_NAME = os.environ.get('SPEEDTEST_EXPORTER_NAME',
                                      'speedtest-exporter')
SPEEDTEST_EXPORTER_LOGLEVEL = os.environ.get('SPEEDTEST_EXPORTER_LOGLEVEL',
                                             'INFO').upper()

# Logging Configuration
try:
    logging.basicConfig(stream=sys.stdout,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S',
                        level=SPEEDTEST_EXPORTER_LOGLEVEL)
except ValueError:
    logging.basicConfig(stream=sys.stdout,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S',
                        level='INFO')
    logging.error("SPEEDTEST_EXPORTER_LOGLEVEL invalid !")
    sys.exit(1)

try:
    SPEEDTEST_EXPORTER_PORT = int(os.environ.get('SPEEDTEST_EXPORTER_PORT', '8123'))
except ValueError:
    logging.error("SPEEDTEST_EXPORTER_PORT must be int !")
    sys.exit(1)

METRICS = [
    {'name': 'download', 'description': 'Speedtest Download Speed in bit/s', 'type': 'gauge'},
    {'name': 'ping', 'description': 'Speedtest Ping in ms', 'type': 'gauge'},
    {'name': 'upload', 'description': 'Speedtest Upload Speed in bit/s', 'type': 'gauge'}
]

# REGISTRY Configuration
REGISTRY.unregister(PROCESS_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
REGISTRY.unregister(REGISTRY._names_to_collectors['python_gc_objects_collected_total'])

class SpeedtestCollector():
    '''Speedtest Collector Class'''
    def __init__(self):
        self.speedtest = speedtest.Speedtest()

    def get_data(self):
        '''Get Speedtest Data'''
        # Init Default Dicts
        labels = defaultdict(dict)
        data = defaultdict(dict)

        # Job
        labels['job'] = SPEEDTEST_EXPORTER_NAME

        # Collect Speedtest Data
        self.speedtest.get_servers()
        self.speedtest.get_best_server()
        self.speedtest.download()
        self.speedtest.upload()
        res = self.speedtest.results.dict()

        # Speedtest Distance Between Client & Server
        labels['distance'] = res['server']['d']

        # Speedtest Server Latitude
        labels['server_latitude'] =  res['server']['lat']
        # Speedtest Server Longitude
        labels['server_longitude'] =  res['server']['lon']
        # Speedtest Server Name
        labels['server_name'] =  res['server']['name']
        # Speedtest Server Country
        labels['server_country'] =  res['server']['cc']
        # Speedtest Server ID
        labels['server_id'] =  res['server']['id']

        # Speedtest Client IP
        labels['client_ip'] =  res['client']['ip']
        # Speedtest Client Latitude
        labels['client_latitude'] =  res['client']['lat']
        # Speedtest Client Longitude
        labels['client_longitude'] =  res['client']['lon']
        # Speedtest Client ISP
        labels['client_isp'] =  res['client']['isp']
        # Speedtest Client ISP
        labels['client_country'] =  res['client']['country']

        # Speedtest Download
        data['download'] = res['download']
        # Speedtest Ping
        data['ping'] = res['ping']
        # Speedtest Upload
        data['upload'] = res['upload']

        return labels, data

    def collect(self):
        '''Collect Prometheus Metrics'''
        # Get Data
        labels, data = self.get_data()
        logging.info('Labels : %s.', dict(labels))
        logging.info('Data : %s.', dict(data))
        # Forge Prometheus Metrics
        metrics = []
        for key, value in data.items():
            if key in labels.keys():
                continue
            description = [i['description'] for i in METRICS if key == i['name']][0]
            metric_type = [i['type'] for i in METRICS if key == i['name']][0]
            metrics.append({'name': f'speedtest_{key.lower()}',
                            'value': int(value),
                            'description': description,
                            'type': metric_type
                          })
        # Return Prometheurs Metrics
        for metric in metrics:
            prometheus_metric = Metric(metric['name'], metric['description'], metric['type'])
            prometheus_metric.add_sample(metric['name'], value=metric['value'], labels=labels)
            yield prometheus_metric

def main():
    '''Main Function'''
    logging.info("Starting Speedtest Exporter on port %s.", SPEEDTEST_EXPORTER_PORT)
    logging.debug("SPEEDTEST_EXPORTER_PORT: %s.", SPEEDTEST_EXPORTER_PORT)
    logging.debug("SPEEDTEST_EXPORTER_NAME: %s.", SPEEDTEST_EXPORTER_NAME)
    # Start Prometheus HTTP Server
    start_http_server(SPEEDTEST_EXPORTER_PORT)
    # Init HueMotionSensorCollector
    REGISTRY.register(SpeedtestCollector())
    # Loop Infinity
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
