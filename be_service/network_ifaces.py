import netifaces
import logging 
import subprocess
from ipaddress import IPv4Network

class NetworkIface():
    ''' Root class for networkifaces '''
    def __init__(self, ifname: str) -> None:
        self.ifname = ifname
        self.ipv4 = {"conn_status": False, "addr": "", "netmask": "", "broadcast": ""}
        self.ipv6 = {"addr": "", "netmask": ""}
        self.mac_addr = {"addr": ""}
        self.get_interface_parameter()

    def get_interface_parameter(self):
        '''
        Get the current information from the interface
        ''' 
        if self.ifname not in netifaces.interfaces():
            logging.debug(f'Interface {self.ifname} no found')
            return
        
        addrs = netifaces.ifaddresses(self.ifname)
        if netifaces.AF_INET in addrs:
            ipv4_info = addrs[netifaces.AF_INET]
            self.ipv4["conn_status"] = True
            for key, value in ipv4_info[0].items():
                self.ipv4[key] = value

        if netifaces.AF_INET6 in addrs:
            ipv6_info = addrs[netifaces.AF_INET6]
            for key, value in ipv6_info[0].items():
                self.ipv6[key] = value

        if netifaces.AF_LINK in addrs:
            mac_info = addrs[netifaces.AF_LINK]
            for key, value in mac_info[0].items():
                self.mac_addr[key] = value

        logging.debug(f'Get information from interface: {self.ifname}')


    def get_ipv4_info(self) -> dict:
        '''
        Return ipv4 information from the interface as dictionary 
        '''
        return self.ipv4
    
    def get_ipv6_info(self) -> dict:
        '''
        Return ipv6 information from the interface as dictionary 
        '''
        return self.ipv6
    
    def get_mac_info(self) -> dict:
        '''
        Return mac-address information from the interface as dictionary
        '''
        return self.mac_addr
    
    def get_interface_info(self) -> dict:
        '''
        Return all the information from the interface as dictionary
        '''
        return {"ipv4": self.get_ipv4_info(),
                "ipv6": self.get_ipv6_info(),
                "link": self.get_mac_info()}
    
    def write_config(self, config_txt, filename):
        '''
        Write configuration to a file indicate by filename and 
        force the restart of NetworkManager
        '''
        try:
            with open(filename,'w') as file:
                file.write(config_txt)
        except IOError:
            logging.warning(f'Config file {filename} not found!')
            return None
        
        return self.restart_network_manager()

    def restart_network_manager(self):
        return subprocess.Popen("systemctl restart NetworkManager", shell=True)
    


class EthernetIface(NetworkIface):
    NM_CONFIG_FILE="/etc/NetworkManager/system-connections/wired.nmconnection"
    NM_CONFIG_TEMPLATE="""
[connection]
id=wired
uuid=83470bf3-2346-423c-84c2-6e2ce0e0c74e
type=ethernet
autoconnect=true
autoconnect-priority=999
interface-name=eth1

[ethernet]

[ipv4]
method=manual
address1={ipaddr}/{prefix}
gateway={gateway}

[ipv6]
method=auto
addr-gen-mode=stable-privacy
ip6-privacy=0
"""
    def get_interface_info(self) -> dict:
        '''
        Get all the information available for Ethernet interface and return as Dictionary
        '''
        response = super().get_interface_info()
        logging.debug(f'Ethernet Interface: {self.ifname} \n Information: {response}')
        return response
    
    def config_ethertnet(self,ipaddr="192.168.30.1" ,
                         netmask="255.255.255.0",
                         gateway="192.168.30.254") -> bool:
        '''
        This method create the NetWork Manager config file, write the it and restart 
        Network Manager to read the new config file. 
        '''
        nm_config = self.NM_CONFIG_TEMPLATE.format(
                ipaddr=ipaddr,
                prefix=IPv4Network(f"0.0.0.0/{netmask}").prefixlen,
                gateway=gateway
        )

        logging.debug(f'Ethernet interface: {self.ifname} \
                      configuration request with: \n\
                      ip addr:{ipaddr} netmask:{netmask} gateway:{gateway}')
        result = self.write_config(nm_config,self.NM_CONFIG_FILE)
        return False if result == None else True

        

class WiFiIface(NetworkIface):
    NMCLI_CMD_ARGS=[
        'nmcli',
        '-t',
        '-s',
        '-f',
        '802-11-wireless.ssid,802-11-wireless.channel,\
            802-11-wireless-security.key-mgmt,802-11-wireless-security.psk',
        'con',
        'show',
        'wireless'
    ]
    NM_CONFIG_FILE="/etc/NetworkManager/system-connections/wireless.nmconnection"
    NM_CONFIG_TEMPLATE="""
[connection]
id=wireless
uuid=29883662-1f5e-4e24-aa6c-f3fd03123a75
type=wifi
interface-name=wlan0

[wifi]
band=bg
channel={channel}
mode=ap
ssid={ssid}

[wifi-security]
key-mgmt={crypt}
psk={password}

[ipv4]
address1={ipaddr}/{prefix}
method=shared

[ipv6]
addr-gen-mode=stable-privacy
method=auto

[proxy]
"""

    def __init__(self, ifname: str) -> None:
        super().__init__(ifname)
        self.ssid = ""
        self.password = ""
        self.encrypt = ""
        self.channel = 3
        self.get_wifi_parameters()

    def get_wifi_parameters(self):
        try:
            output = subprocess.run(self.NMCLI_CMD_ARGS, capture_output=True, text=True)
            if output.returncode == 0:
                output_stdout = output.stdout
                print(output_stdout)
                print(output_stdout.split(':'))
        except:
            logging.error('Fetching information from Network Manager for wifi interface')


    def get_wifi_info(self) -> dict:
        '''
        Return specific information for wifi interface as dictionary
        '''
        return {"ssid": self.ssid,
                "password": self.password,
                "encrypt": self.encrypt,
                "channel": self.channel}

    def get_interface_info(self) -> dict:
        '''
        Return all information from a wifi interface
        '''
        response = super().get_interface_info()
        response["wifi_conf"] = self.get_wifi_info()
        logging.debug(f'WiFi Interface: ${self.ifname} \n Information: ${response}')
        return response

    def config_wifi(self, 
                    ipaddr="192.168.100.1", 
                    netmask="255.255.255.0",
                    ssid="ARCTURUS_WIFI", 
                    password="arcturus123",
                    crypt="wpa-psk",
                    channel=3) -> bool:
        '''
        Change the configuration for wifi interface
        '''
        nm_config = self.NM_CONFIG_TEMPLATE.format(
                ipaddr=ipaddr,
                prefix=IPv4Network(f"0.0.0.0/{netmask}").prefixlen,
                ssid=ssid,
                crypt=crypt,
                password=password,
                channel=channel
        )

        logging.debug(f'Ethernet interface: {self.ifname} \
                      configuration request with: \n\
                      ip addr:{ipaddr} netmask:{netmask} ssid={ssid} \
                      crypt:{crypt} password: {password} channel: {channel}')
        result = self.write_config(nm_config, self.NM_CONFIG_FILE)
        return False if result == None else True



class LTEIface(NetworkIface):
    NMCLI_CMD_ARGS=[
        'nmcli',
        '-t',
        '-s',
        '-f',
        'gsm.apn',
        'con',
        'show',
        'wireless'
    ]
    NM_CONFIG_FILE="/etc/NetworkManager/system-connections/lte-modem.nmconnection"
    NM_CONFIG_TEMPLATE="""
[connection]
id=lte-modem
uuid=4f91b966-ce9b-4690-835b-342f031fd7f0
type=gsm
autoconnect=true

[gsm]
apn={apn}

[serial]
baud=115200

[ipv4]
method=auto

[ipv6]
method=ignore

[ppp]
lcp-echo-failure=5
lcp-echo-interval=30
refuse-eap=true
refuse-pap=false
refuse-chap=false
refuse-mschap=false
refuse-mschapv2=false
"""

    def __init__(self, ifname: str) -> None:
        super().__init__(ifname)
        self.apn = ""
        self.signal = 0
        self.get_lte_parameter()

    def get_lte_parameter(self):
        try:
            output = subprocess.run(self.NMCLI_CMD_ARGS, capture_output=True, text=True)
            if output.returncode == 0:
                self.apn = output.stdout.split(':')[1]
                print(self.apn)
        except:
            logging.error('Fetching information from Network Manager for lte interface')

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

    def config_lte(self, apn="timbrasil.br"):
        nm_config = self.NM_CONFIG_TEMPLATE.format(apn=apn )

        logging.debug(f'LTE interface: {self.ifname} \
                      configuration request with: \n\
                      apn:{apn}')
        result = self.write_config(nm_config,self.NM_CONFIG_FILE)
        return False if result == None else True
