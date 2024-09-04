import scapy.all as scapy
import psutil
from threading import Thread
from app.database import log_incidents

def detect_arp_spoofing(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = scapy.getmacbyip(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            if real_mac != response_mac:
                log_incident("ARP Spoofing", f"{packet[scapy.ARP].psrc} is conflicting with {packet[scapy.ARP].hwsrc}")
                print(f"ARP Spoofing Detected: {packet[scapy.ARP].psrc} is conflicting with {packet[scapy.ARP].hwsrc}")
        except Exception as e:
            pass

def monitor_network_usage():
    threshold = 1000000  # 1MB threshold for DDoS detection
    while True:
        bytes_received = psutil.net_io_counters().bytes_recv
        if bytes_received > threshold:
            log_incident("DDoS Attack", f"Bytes received: {bytes_received}")
            print("Potential DDoS Attack Detected")
        # Add a delay to prevent excessive CPU usage
        time.sleep(1)

def detect_port_scanning(packet):
    if packet.haslayer(scapy.TCP) and packet[scapy.TCP].flags == "S":
        src_ip = packet[scapy.IP].src
        dst_port = packet[scapy.TCP].dport
        log_incident("Port Scanning", f"Source IP: {src_ip} is scanning port {dst_port}")
        print(f"Port Scanning Detected: Source IP {src_ip} is scanning port {dst_port}")

def start_detection():
    # Start the ARP spoofing detection in a separate thread
    arp_thread = Thread(target=scapy.sniff, kwargs={"prn": detect_arp_spoofing, "store": False})
    arp_thread.start()

    # Start the DDoS monitoring in another thread
    ddos_thread = Thread(target=monitor_network_usage)
    ddos_thread.start()

    # Start the Port Scanning detection in another thread
    port_scan_thread = Thread(target=scapy.sniff, kwargs={"prn": detect_port_scanning, "store": False})
    port_scan_thread.start()
