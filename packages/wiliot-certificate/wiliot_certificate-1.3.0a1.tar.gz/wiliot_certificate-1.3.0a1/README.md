# wiliot-certificate #

<!-- Description -->
wiliot-certificate is a python library with tools used to test & certify boards and their compatibility with Wiliot's echosystem.
This python package includes the following CLI utilities:
 - Gateway Certificate (`wlt-gw-certificate`)

## Installing wiliot-certificate
````commandline
pip install wiliot-certificate
````

## Using wiliot-certificate
### Gateway Certificate
Test Wiliot GWs capabilities.
The GW Certificate includes different test that run sequentially to test each capability reported by the GW.
To run the GW Certificate the GW needs to use a public MQTT Broker (Eclipse):

Host:	mqtt.eclipseprojects.io
TLS TCP Port:	8883
TLS Websocket Port:	443
TCP Port:	1883
Websocket Port:	80

More information can be found at https://mqtt.eclipseprojects.io/.

#### Connection Test
Processes status packet sent by the GW to the MQTT Broker and validates it according to API Version.

#### Uplink Test
Simulates Wiliot MEL and validates that data is uploaded correctly to the cloud.

#### Downlink Test
Sends advertising actions (txPacket) via MQTT to the GW and validates their advertisements.

#### Stress Test
Increments time delays between packets to evaluate GW's capability in handling increasing packets per second rates.

#### GW Certificate Release Notes:
1.3.0:
 - Released in a standalone wiliot-certificate package
 - Python 3.13 support
 - Gw API version 205 support
 - Registration Test


```
usage: wlt-gw-certificate [-h] -owner OWNER -gw GW [-suffix SUFFIX] [-tests {connection,uplink,downlink,stress}]

Gateway Certificate - CLI Tool to test Wiliot GWs

required arguments:
  -gw GW        Gateway ID
  -owner OWNER  Owner ID (optional when running only the registration test)

optional arguments:
  -suffix       Allow for different suffixes after the GW ID in MQTT topics
  -tests        Pick specific tests to run
  -update       Update the firmware of the test board
  -pps          Pick specific PPS rate for the stress test
  -agg          Time the uplink stages should wait before processing packets
  -h, --help    show this help message and exit
  ```
