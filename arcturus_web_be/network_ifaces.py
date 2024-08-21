import netifaces
import os

def get_ethenet_info():
    response = {"connection":"false", 
                "ipaddr":"",
                "netmask":"",
                "broadcast":""}
    
    iface = netifaces.ifaddresses("eth1")
    if iface != None:
        response["connection"] = "true"
        response["ipaddr"] = iface[netifaces.AF_INET]["addr"]
        response["netmask"] = iface[netifaces.AF_INET]["netmask"]
        response["broadcast"] = iface[netifaces.AF_INET]["broadcast"]
    
    return response

def get_wifi_info():
    pass

def get_lte_info():
    pass

def set_ethernet_conf(connection: bool, 
                      ipaddr: str, 
                      netmask: str, 
                      broadcast: str):
    pass


def set_wifi_conf(connection: bool, 
                  ipaddr: str, 
                  netmask: str, 
                  broadcast: str, 
                  ssid: str, 
                  password: str):
    pass

def set_lte_conf(connection: bool, 
                 apn: str):
    pass
