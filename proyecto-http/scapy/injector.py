
from scapy.all import *

# 1er Fuzzing: URL larguísima
ip1 = IP(dst="127.0.0.1")
tcp1 = TCP(dport=8080, sport=RandShort(), flags="S")
payload = "GET /" + "A"*5000 + " HTTP/1.1\r\nHost: servidor\r\n\r\n"
pkt1 = ip1/tcp1/Raw(load=payload)
send(pkt1)
print("Inyección 1 enviada")

# 2do Fuzzing: Método HTTP inválido
ip2 = IP(dst="172.0.0.1")
tcp2 = TCP(dport=8080, sport=RandShort(), flags="S")
payload2 = "GET / HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n"

pkt2 = ip2/tcp2/Raw(load=payload2)
send(pkt2)
print("Inyeccion 2 enviada")
