#.!/usr/bin/env python3
#coding: utf-8

'''Speedtest Exporter'''

from subprocess import check_output, STDOUT, CalledProcessError
from json import loads
from json.decoder import JSONDecodeError
import sys
import logging
import os
from time import sleep
from collections import defaultdict
from prometheus_client.core import REGISTRY, Metric
from prometheus_client import start_http_server, PROCESS_COLLECTOR, PLATFORM_COLLECTOR

# Exporter Name Definition
SPEEDTEST_EXPORTER_NAME = os.environ.get('SPEEDTEST_EXPORTER_NAME',
                                         'speedtest-exporter')

# Exporter Log Level Definition
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

# Exporter Port Check
try:
    SPEEDTEST_EXPORTER_PORT = int(os.environ.get('SPEEDTEST_EXPORTER_PORT', '8123'))
except ValueError:
    logging.error("SPEEDTEST_EXPORTER_PORT must be int !")
    sys.exit(1)

# Metrics Definition
METRICS = [
    {'name': 'ping_jitter',
     'description': 'Speedtest Ping Jitter in ms.',
     'type': 'gauge'},
    {'name': 'ping_latency',
     'description': 'Speedtest Ping Latency in ms.',
     'type': 'gauge'},
    {'name': 'ping_low',
     'description': 'Speedtest Ping Low in ms.',
     'type': 'gauge'},
    {'name': 'ping_high',
     'description': 'Speedtest Ping High in ms.',
     'type': 'gauge'},
    {'name': 'download_bandwidth',
     'description': 'Speedtest Download Bandwith in bytes per second (B/s).',
     'type': 'gauge'},
    {'name': 'download_bytes',
     'description': 'Speedtest Download Bytes in bytes.',
     'type': 'gauge'},
    {'name': 'download_elapsed',
     'description': 'Speedtest Download Elapsed in ms.',
     'type': 'gauge'},
    {'name': 'download_latency_iqm',
     'description': 'Speedtest Download IQM Latency in ms.',
     'type': 'gauge'},
    {'name': 'download_latency_low',
     'description': 'Speedtest Download Low Latency in ms.',
     'type': 'gauge'},
    {'name': 'download_latency_high',
     'description': 'Speedtest Download High Latency in ms.',
     'type': 'gauge'},
    {'name': 'download_latency_jitter',
     'description': 'Speedtest Download Jitter Latency in ms.',
     'type': 'gauge'},
    {'name': 'upload_bandwidth',
     'description': 'Speedtest Upload Bandwith in bytes per second (B/s).',
     'type': 'gauge'},
    {'name': 'upload_bytes',
     'description': 'Speedtest Upload Bytes in bytes.',
     'type': 'gauge'},
    {'name': 'upload_elapsed',
     'description': 'Speedtest Upload Elapsed in ms.',
     'type': 'gauge'},
    {'name': 'upload_latency_iqm',
     'description': 'Speedtest Upload IQM Latency in ms.',
     'type': 'gauge'},
    {'name': 'upload_latency_low',
     'description': 'Speedtest Upload Low Latency in ms.',
     'type': 'gauge'},
    {'name': 'upload_latency_high',
     'description': 'Speedtest Upload High Latency in ms.',
     'type': 'gauge'},
    {'name': 'upload_latency_jitter',
     'description': 'Speedtest Upload Jitter Latency in ms.',
     'type': 'gauge'},
    {'name': 'packet_loss',
     'description': 'Speedtest Percentage of Packet Loss during test.',
     'type': 'gauge'}
]

# REGISTRY Configuration
REGISTRY.unregister(PROCESS_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
REGISTRY.unregister(REGISTRY._names_to_collectors['python_gc_objects_collected_total'])

# Speedtest Class
class SpeedtestCollector():
    '''Speedtest Collector Class'''
    def __init__(self):
        pass

    def run_speedtest(self):
        '''Run Speedtest & Return JSON Results or Exit'''
        try:
            speedtest_cmd = check_output(['speedtest',
                                          '--accept-license',
                                          '--accept-gdpr',
                                          '-f',
                                          'json'],
                                         stderr=STDOUT,
                                         text=True)
            logging.debug(speedtest_cmd)
            return loads(speedtest_cmd)
        except CalledProcessError as exception:
            logging.error(loads(exception.output)['message'])
            sys.exit(1)
        except JSONDecodeError as exception:
            logging.error(exception)
            sys.exit(1)

    @staticmethod
    def _parse_results(res):
        labels = defaultdict(dict)
        datas = defaultdict(dict)
        labels['isp'] = res['isp']
        labels['interface_name'] = res['interface']['name']
        labels['interface_internal_ip'] = res['interface']['internalIp']
        labels['interface_external_ip'] = res['interface']['externalIp']
        labels['interface_mac_address'] = res['interface']['macAddr']
        labels['interface_is_vpn'] = str(res['interface']['isVpn'])
        labels['server_id'] = str(res['server']['id'])
        labels['server_host'] = res['server']['host']
        labels['server_port'] = str(res['server']['port'])
        labels['server_name'] = res['server']['name']
        labels['server_location'] = res['server']['location']
        labels['server_country'] = res['server']['country']
        labels['server_ip'] = res['server']['ip']
        labels['result_id'] = res['result']['id']
        labels['result_url'] = res['result']['url']
        labels['result_persisted'] = str(res['result']['persisted'])
        datas['ping_jitter'] = res['ping']['jitter']
        datas['ping_latency'] = res['ping']['latency']
        datas['ping_low'] = res['ping']['low']
        datas['ping_high'] = res['ping']['high']
        datas['download_bandwidth'] = res['download']['bandwidth']
        datas['download_bytes'] = res['download']['bytes']
        datas['download_elapsed'] = res['download']['elapsed']
        datas['download_latency_iqm'] = res['download']['latency']['iqm']
        datas['download_latency_low'] = res['download']['latency']['low']
        datas['download_latency_high'] = res['download']['latency']['high']
        datas['download_latency_jitter'] = res['download']['latency']['jitter']
        datas['upload_bandwidth'] = res['download']['bandwidth']
        datas['upload_bytes'] = res['upload']['bytes']
        datas['upload_elapsed'] = res['upload']['elapsed']
        datas['upload_latency_iqm'] = res['upload']['latency']['iqm']
        datas['upload_latency_low'] = res['upload']['latency']['low']
        datas['upload_latency_high'] = res['upload']['latency']['high']
        datas['upload_latency_jitter'] = res['upload']['latency']['jitter']
        datas['packet_loss'] = res['packetLoss']
        return labels, datas

    def collect(self):
        '''Collect & Return Prometheus Metrics'''
        # Get Labels & Datas
        labels, datas = self._parse_results(self.run_speedtest())
        logging.info('Labels : %s.', dict(labels))
        logging.info('Datas : %s.', dict(datas))
        # Forge Prometheus Metrics
        metrics = []
        for key, value in datas.items():
            if key in labels.keys():
                continue
            description = [i['description'] for i in METRICS if key == i['name']][0]
            metric_type = [i['type'] for i in METRICS if key == i['name']][0]
            metrics.append({'name': f'speedtest_{key.lower()}',
                            'value': float(value),
                            'description': description,
                            'type': metric_type
                          })
        # Return Prometheurs Metrics
        for metric in metrics:
            prometheus_metric = Metric(metric['name'], metric['description'], metric['type'])
            prometheus_metric.add_sample(metric['name'], value=metric['value'], labels=labels)
            yield prometheus_metric

# Main Function
def main():
    '''Main Function'''
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
if __name__ == '__main__':
    main()
