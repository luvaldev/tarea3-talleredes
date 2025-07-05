from scapy.all import *

# Modificación 1: Host inválido
ip = IP(dst="127.0.0.1")
tcp = TCP(dport=8080, sport=RandShort(), flags="S")
payload = "GET / HTTP/1.1\r\nHost: noexiste\r\n\r\n"
pkt = ip/tcp/Raw(load=payload)
send(pkt)
print("Modificación 1 enviada")

# Modificación 2: User-Agent extraño
payload2 = "GET / HTTP/1.1\r\nHost: servidor\r\nUser-Agent: 𝔘𝔫𝔦𝔠𝔬𝔡𝔢💥\r\n\r\n"
pkt2 = ip/tcp/Raw(load=payload2)
send(pkt2)
print("Modificación 2 enviada")

# Modificación 3: Cambiar método a DELETE
payload3 = "DELETE / HTTP/1.1\r\nHost: servidor\r\n\r\n"
pkt3 = ip/tcp/Raw(load=payload3)
send(pkt3)
print("Modificación 3 enviada")
