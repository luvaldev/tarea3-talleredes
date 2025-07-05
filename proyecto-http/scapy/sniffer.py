
from scapy.all import *

def mostrar_paquete(pkt):
	pkt.show()

sniff(filter="tcp port 8080", prn=mostrar_paquete)
