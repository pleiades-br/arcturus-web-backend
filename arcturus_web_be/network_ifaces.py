import netifaces
import os
import re

class NetworkIface():
    ''' Root class for networkifaces '''
    def __init__(self, ifname: str) -> None:
        self.ifname = ifname
        self.conn_status = False
        self.ipv4_ipaddr = ""
        self.ipv4_netmask = ""
        self.ipv4_broadcast = ""
        self.ipv6_ipaddr = ""
        self.ipv6_netmask = ""
        self.mac_addr = ""

    def __enter__(self): 
        addrs = netifaces.ifaddresses(self.ifname)
        ipv4_info = netifaces.AF_INET in addrs
        if ipv4_info:
            self.conn_status = True
            self.ipv4_ipaddr = ipv4_info[0]["addr"]
            self.ipv4_netmask  = ipv4_info[0]["netmask"]
            self.ipv4_broadcast = ipv4_info[0]["broadcast"]

        ipv6_info = netifaces.AF_INET6 in addrs
        if ipv6_info:
            self.ipv6_ipaddr = ipv6_info[0]["addr"]
            self.ipv6_netmask = ipv6_info[0]["netmask"]

        mac_info = netifaces.AF_LINK in addrs
        if mac_info:
            self.mac_addr = mac_info[0]["addr"]

    def get_ipv4_info(self) -> dict:
        '''Return ipv4 information from the interface as dictionary '''
        return {"connection_state": self.conn_status, 
                "addr": self.ipv4_ipaddr,
                "netmask": self.ipv4_netmask,
                "broadcast": self.ipv4_broadcast}
    
    def get_ipv6_info(self) -> dict:
        '''Return ipv6 information from the interface as dictionary '''
        return {"addr": self.ipv6_ipaddr,
                "netmask": self.ipv6_netmask}
    
    def get_mac_info(self) -> dict:
        '''Return mac-address information from the interface as dictionary'''
        return {"addr": self.mac_addr}
    

class EthernetIface(NetworkIface):
    def config_ethertnet(self, ipaddr: str, netmask: str):
        pass


class WiFiIface(NetworkIface):
    def __init__(self, ifname: str) -> None:
        super().__init__(ifname)
        self.ssid = ""
        self.password = ""
        self.encrypt = ""

    def get_wifi_info(self) -> dict:
        '''Return specific information for wifi interface as dictionary'''
        return {"ssid": self.ssid,
                "password": self.password,
                "encrypt": self.encrypt}

    def config_wifi(self, ipaddr: str, netmask: str, ssid: str, password: str, crypt: str):
        '''Change the configuration for wifi interface'''
        pass

class LTEIface(NetworkIface):
    def __init__(self, ifname: str) -> None:
        super().__init__(ifname)
        self.apn = ""
        self.signal = 0

    def get_lte_info(self) -> dict:
        '''Return specific information for LTE interface as dictionary'''
        return {"apn": self.apn,
                "signal_quality": self.signal}

    def config_lte(self, apn: str):
        pass
