# Speedtest Exporter

## Quick Start

```bash
DOCKER_BUILDKIT=1 docker build -t speedtest-exporter .
docker run -dit --name speedtest-exporter speedtest-exporter
```

## Metrics

```bash
# HELP speedtest_ping_jitter Speedtest Ping Jitter in ms.
# TYPE speedtest_ping_jitter gauge
speedtest_ping_jitter{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 0.482
# HELP speedtest_ping_latency Speedtest Ping Latency in ms.
# TYPE speedtest_ping_latency gauge
speedtest_ping_latency{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 1.357
# HELP speedtest_ping_low Speedtest Ping Low in ms.
# TYPE speedtest_ping_low gauge
speedtest_ping_low{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 0.919
# HELP speedtest_ping_high Speedtest Ping High in ms.
# TYPE speedtest_ping_high gauge
speedtest_ping_high{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 1.913
# HELP speedtest_download_bandwidth Speedtest Download Bandwidth in bytes per second (B/s).
# TYPE speedtest_download_bandwidth gauge
speedtest_download_bandwidth{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 2.780559e+07
# HELP speedtest_download_bytes Speedtest Download Bytes in bytes.
# TYPE speedtest_download_bytes gauge
speedtest_download_bytes{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 1.45185168e+08
# HELP speedtest_download_elapsed Speedtest Download Elapsed in ms.
# TYPE speedtest_download_elapsed gauge
speedtest_download_elapsed{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 5201.0
# HELP speedtest_download_latency_iqm Speedtest Download IQM Latency in ms.
# TYPE speedtest_download_latency_iqm gauge
speedtest_download_latency_iqm{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 34.535
# HELP speedtest_download_latency_low Speedtest Download Low Latency in ms.
# TYPE speedtest_download_latency_low gauge
speedtest_download_latency_low{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 2.25
# HELP speedtest_download_latency_high Speedtest Download High Latency in ms.
# TYPE speedtest_download_latency_high gauge
speedtest_download_latency_high{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 48.137
# HELP speedtest_download_latency_jitter Speedtest Download Jitter Latency in ms.
# TYPE speedtest_download_latency_jitter gauge
speedtest_download_latency_jitter{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 4.139
# HELP speedtest_upload_bandwidth Speedtest Upload Bandwidth in bytes per second (B/s).
# TYPE speedtest_upload_bandwidth gauge
speedtest_upload_bandwidth{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 2.7167284e+07
# HELP speedtest_upload_bytes Speedtest Upload Bytes in bytes.
# TYPE speedtest_upload_bytes gauge
speedtest_upload_bytes{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 1.27380307e+08
# HELP speedtest_upload_elapsed Speedtest Upload Elapsed in ms.
# TYPE speedtest_upload_elapsed gauge
speedtest_upload_elapsed{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 4612.0
# HELP speedtest_upload_latency_iqm Speedtest Upload IQM Latency in ms.
# TYPE speedtest_upload_latency_iqm gauge
speedtest_upload_latency_iqm{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 13.764
# HELP speedtest_upload_latency_low Speedtest Upload Low Latency in ms.
# TYPE speedtest_upload_latency_low gauge
speedtest_upload_latency_low{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 6.307
# HELP speedtest_upload_latency_high Speedtest Upload High Latency in ms.
# TYPE speedtest_upload_latency_high gauge
speedtest_upload_latency_high{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 246.942
# HELP speedtest_upload_latency_jitter Speedtest Upload Jitter Latency in ms.
# TYPE speedtest_upload_latency_jitter gauge
speedtest_upload_latency_jitter{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 7.949
# HELP speedtest_packet_loss Speedtest Percentage of Packet Loss during test.
# TYPE speedtest_packet_loss gauge
speedtest_packet_loss{interface_external_ip="83.197.193.12",interface_internal_ip="172.18.0.24",interface_is_vpn="False",interface_mac_address="02:42:AC:12:00:18",interface_name="eth0",isp="Orange",result_id="c812fcce-1ca1-4909-96f2-4a35475c8418",result_persisted="True",result_url="https://www.speedtest.net/result/c/c812fcce-1ca1-4909-96f2-4a35475c8418",server_country="France",server_host="rennes3.speedtest.orange.fr",server_id="23282",server_ip="80.12.26.64",server_location="Rennes",server_name="ORANGE FRANCE",server_port="8080"} 0.0
```
