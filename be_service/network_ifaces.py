import netifaces
import logging 
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
        self.collect_interface_info()

    def collect_interface_info(self): 
        if self.ifname not in netifaces.interfaces():
            logging.debug(f'Interface {self.ifname} no found')
            return
        
        addrs = netifaces.ifaddresses(self.ifname)
        if netifaces.AF_INET in addrs:
            ipv4_info = addrs[netifaces.AF_INET]
            self.conn_status = True
            self.ipv4_ipaddr = ipv4_info[0]["addr"]
            self.ipv4_netmask  = ipv4_info[0]["netmask"]
            self.ipv4_broadcast = ipv4_info[0]["broadcast"]

        if netifaces.AF_INET6 in addrs:
            ipv6_info = addrs[netifaces.AF_INET6]
            self.ipv6_ipaddr = ipv6_info[0]["addr"]
            self.ipv6_netmask = ipv6_info[0]["netmask"]

        if netifaces.AF_LINK in addrs:
            mac_info = addrs[netifaces.AF_LINK]
            self.mac_addr = mac_info[0]["addr"]

        logging.debug(f'Get information from interface: {self.ifname}')

    def get_ipv4_info(self) -> dict:
        '''
        Return ipv4 information from the interface as dictionary 
        '''
        return {"connection_state": self.conn_status, 
                "addr": self.ipv4_ipaddr,
                "netmask": self.ipv4_netmask,
                "broadcast": self.ipv4_broadcast}
    
    def get_ipv6_info(self) -> dict:
        '''
        Return ipv6 information from the interface as dictionary 
        '''
        return {"addr": self.ipv6_ipaddr,
                "netmask": self.ipv6_netmask}
    
    def get_mac_info(self) -> dict:
        '''
        Return mac-address information from the interface as dictionary
        '''
        return {"addr": self.mac_addr}
    
    def get_interface_info(self) -> dict:
        '''
        Return all the information from the interface as dictionary
        '''
        return {"ipv4": self.get_ipv4_info(),
                "ipv6": self.get_ipv6_info(),
                "link": self.get_mac_info()}
    

class EthernetIface(NetworkIface):
    def get_interface_info(self) -> dict:
        response = super().get_interface_info()
        logging.debug(f'Ethernet Interface: {self.ifname} \n Information: {response}')
        return response
    
    def config_ethertnet(self, ipaddr: str, netmask: str):
        pass


class WiFiIface(NetworkIface):
    def __init__(self, ifname: str) -> None:
        super().__init__(ifname)
        self.ssid = ""
        self.password = ""
        self.encrypt = ""

    def get_wifi_info(self) -> dict:
        '''
        Return specific information for wifi interface as dictionary
        '''
        return {"ssid": self.ssid,
                "password": self.password,
                "encrypt": self.encrypt}

    def get_interface_info(self) -> dict:
        '''
        Return all information from a wifi interface
        '''
        response = super().get_interface_info()
        response["wifi_conf"] = self.get_wifi_info()
        logging.debug(f'WiFi Interface: ${self.ifname} \n Information: ${response}')
        return response

    def config_wifi(self, ipaddr: str, netmask: str, ssid: str, password: str, crypt: str):
        '''
        Change the configuration for wifi interface
        '''
        pass


class LTEIface(NetworkIface):
    def __init__(self, ifname: str) -> None:
        super().__init__(ifname)
        self.apn = ""
        self.signal = 0

    def get_lte_info(self) -> dict:
        '''
        Return specific information for LTE interface as dictionary
        '''
        return {"apn": self.apn,
                "signal_quality": self.signal}
    
    def get_interface_info(self) -> dict:
        response = super().get_interface_info()
        response["lte_conf"] = self.get_lte_info()
        logging.debug(f'LTE Interface: {self.ifname} \n Information: {response}')
        return response

    def config_lte(self, apn: str):
        pass
