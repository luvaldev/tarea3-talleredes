from scapy.all import *

# Fuzzing 1
ip1 = IP(dst="127.0.0.1")
tcp1 = TCP(dport=8080, sport=RandShort(), flags="S")
payload1 = "GET /" + "A"*5000 + " HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n"
pkt1 = ip1/tcp1/Raw(load=payload1)
send(pkt1)
print("Fuzzing 1 enviado")

# Fuzzing 2
ip2 = IP(dst="127.0.0.1")
tcp2 = TCP(dport=8080, sport=RandShort(), flags="S")
payload2 = "FUZZ / HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n"
pkt2 = ip2/tcp2/Raw(load=payload2)
send(pkt2)
print("Fuzzing 2 enviado")




---

from scapy.all import *

ip = IP(dst="127.0.0.1")

# Modificación 1: Método DELETE
tcp1 = TCP(dport=8080, sport=RandShort(), flags="S")
payload1 = "DELETE / HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n"
pkt1 = ip/tcp1/Raw(load=payload1)
send(pkt1)
print("[Modificación 1] DELETE enviado")

# Modificación 2: Host inválido
tcp2 = TCP(dport=8080, sport=RandShort(), flags="S")
payload2 = "GET / HTTP/1.1\\r\\nHost: noexiste.local\\r\\n\\r\\n"
pkt2 = ip/tcp2/Raw(load=payload2)
send(pkt2)
print("[Modificación 2] Host inválido enviado")

# Modificación 3: User-Agent alterado
tcp3 = TCP(dport=8080, sport=RandShort(), flags="S")
payload3 = \"GET / HTTP/1.1\\r\\nHost: localhost\\r\\nUser-Agent: 💀🚩🚩\\r\\n\\r\\n\"
pkt3 = ip/tcp3/Raw(load=payload3)
send(pkt3)
print(\"[Modificación 3] User-Agent modificado enviado\")




