#!/usr/bin/env python3
import os
import sys

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"..","be_service"
)
print(SOURCE_PATH)
sys.path.append(SOURCE_PATH)

import network_ifaces as netif 

eth_iface = netif.EthernetIface("eth0")
print(eth_iface.get_interface_info())

wifi_iface = netif.WiFiIface("enps01")
print(wifi_iface.get_interface_info())

LTE_iface = netif.LTEIface("ppp0")
print(LTE_iface.get_interface_info())