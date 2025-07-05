FROM python:3.10-slim

RUN apt-get update && \
	apt-get install -y tcpdump libpcap-dev && \
	pip install scapy

WORKDIR /scapy

COPY sniffer.py sniffer.py
COPY injector.py injector.py
COPY modifier.py modifier.py

CMD ["sleep", "infinity"]
