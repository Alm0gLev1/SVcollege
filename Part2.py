from scapy.all import *


def choose_interface():
    interfaces = get_if_list()
    for i, interface in enumerate(interfaces):
        print(f'{i}: {interface}')

    while True:
        try:
            user_choice = int(input('Choose the interface number from the list above: '))
            if 0 <= user_choice < len(interfaces):
                print(interfaces[user_choice])
                print(type(interfaces[user_choice]))
                return interfaces[user_choice]
            else:
                print('Invalid choice. Try again.')
        except ValueError:
            print('Invalid input. Try again.')


if __name__ == "__main__":
    conf.checkIPaddr = False
    dhcp_discover = Ether(dst='ff:ff:ff:ff:ff:ff', src=RandMAC()) \
                    / IP(src='0.0.0.0', dst='255.255.255.255') \
                    / UDP(sport=68, dport=67) \
                    / BOOTP(op=1, chaddr=RandMAC()) \
                    / DHCP(options=[('message-type', 'discover'), ('end')])

    sendp(dhcp_discover, iface=choose_interface(), loop=1, verbose=1)
