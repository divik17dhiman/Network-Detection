import scapy.all as scapy
import psutil
from threading import Thread
from app.database import log_incident
import time

def detect_arp_spoofing(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = scapy.getmacbyip(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            if real_mac != response_mac:
                log_incident("ARP Spoofing", f"{packet[scapy.ARP].psrc} is conflicting with {packet[scapy.ARP].hwsrc}")
                print(f"[ARP Spoofing Detected] Source IP: {packet[scapy.ARP].psrc}, Response MAC: {packet[scapy.ARP].hwsrc}")
        except Exception as e:
            print("Error detecting ARP spoofing:", e)

def monitor_network_usage():
    threshold = 1000000000000  # 1MB threshold for DDoS detection
    while True:
        bytes_received = psutil.net_io_counters().bytes_recv
        if bytes_received > threshold:
            log_incident("DDoS Attack", f"Bytes received: {bytes_received}")
            print("Potential DDoS Attack Detected")
        time.sleep(1)

def detect_dns_spoofing(packet):
    if packet.haslayer(scapy.DNS) and packet[scapy.DNS].qr == 1:
        dns_query = packet[scapy.DNS].qd.qname.decode()
        dns_response = packet[scapy.DNS].an.rdata.decode() if packet[scapy.DNS].an else "No Answer"
        
        expected_ip = "8.8.8.8"  # Change to a known good DNS server IP
        if dns_response != expected_ip:
            log_incident("DNS Spoofing", f"{dns_query} resolved to {dns_response}, expected {expected_ip}")
            print(f"[DNS Spoofing Detected] Query: {dns_query}, Response: {dns_response}")

def detect_port_scanning():
    open_ports = set()
    while True:
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'ESTABLISHED':
                open_ports.add(conn.laddr.port)
        
        if len(open_ports) > 20:  # Threshold for detecting port scanning
            log_incident("Port Scanning", f"Detected open ports: {open_ports}")
            print(f"[Port Scanning Detected] Open ports: {open_ports}")
        
        time.sleep(5)  # Check every 5 seconds

def start_detection():
    arp_thread = Thread(target=scapy.sniff, kwargs={"prn": detect_arp_spoofing, "store": False})
    arp_thread.daemon = True
    arp_thread.start()

    ddos_thread = Thread(target=monitor_network_usage)
    ddos_thread.daemon = True
    ddos_thread.start()

    dns_thread = Thread(target=scapy.sniff, kwargs={"prn": detect_dns_spoofing, "store": False})
    dns_thread.daemon = True
    dns_thread.start()

    port_scan_thread = Thread(target=detect_port_scanning)
    port_scan_thread.daemon = True
    port_scan_thread.start()
