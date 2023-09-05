# NetworkScan
## Description
This is a simple network scanner that scans the network for devices and displays their IP and MAC addresses. It also displays the vendor of the device. It uses the scapy library to send ARP requests and receive responses. It also us es the argparse library to parse command line arguments.
## Usage
```bash ./main.py -t <target IP address or range>```