from scapy.all import sniff, IP, TCP, UDP

def packet_callback(packet):

    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        protocol = packet[IP].proto

        if TCP in packet:
            payload = packet[TCP].payload
        elif UDP in packet:
            payload = packet[UDP].payload
        else:
            payload = None

        print(f"Source IP: {ip_src}")
        print(f"Destination IP: {ip_dst}")
        print(f"Protocol: {protocol}")
        print(f"Payload: {payload}")
        print("-" * 50)
        
# Sniff packets
sniff(prn=packet_callback, store=0)