
# 📂 Proyecto HTTP + Scapy — Análisis de Protocolo y Manipulación de Tráfico

Este proyecto implementa un entorno de red reproducible basado en **Docker**, compuesto por un **Servidor Apache**, un **Cliente Python** y un contenedor adicional con **Scapy** para interceptar, inyectar y modificar tráfico HTTP.  
El objetivo es simular situaciones de prueba que validen cómo un servicio HTTP responde a tráfico legítimo y a tráfico inesperado o manipulado.

## Video en youtube:

- https://youtu.be/mpaV47ICGGs


## 📌 Estructura del Proyecto

```
proyecto-http/
│
├── docker-compose.yml
│
├── HTML/
│   └── index.html
│
├── cliente/
│   ├── Dockerfile
│   ├── script.py
│
├── scapy/
│   ├── Dockerfile
│   ├── sniffer.py
│   ├── injector.py
│   ├── modifier.py
│
└── README.md
```

## ⚙️ Descripción de los Servicios

### ✅ Servidor Apache (`servidor`)
- Basado en `httpd:latest`.
- Expone el puerto interno `80` al host como `8080`.
- Sirve `index.html` desde la carpeta `HTML/`.

### ✅ Cliente Python (`cliente`)
- Construido sobre `python:3.10-slim`.
- Instala `urllib3` para generar solicitudes HTTP.
- `script.py` realiza una petición `GET` a la raíz `/` del servidor para validar la entrega de contenido.

### ✅ Contenedor Scapy (`scapy`)
- Construido sobre `python:3.10-slim` con `libpcap` y `tcpdump`.
- Configurado con `network_mode: host` para capturar tráfico real de la red del host.
- Ejecuta:
  - `sniffer.py`: Intercepta paquetes que pasan por el puerto `8080`.
  - `injector.py`: Realiza **fuzzing** enviando solicitudes con URLs extremadamente largas y métodos HTTP modificados.
  - `modifier.py`: Envía solicitudes con campos alterados (`Host` inválido, `User-Agent` con símbolos inusuales, método `DELETE`).

## 🚦 Cómo Funciona Todo

1. **Preparación**:  
   - Ejecutar `docker-compose build` para construir las imágenes.  
   - Levantar la infraestructura con `docker-compose up -d`.

2. **Prueba normal**:  
   - El cliente Python envía una solicitud `GET` al servidor.
   - Apache responde con el contenido de `index.html`.
   - Validar con `docker logs cliente_http`.

3. **Captura de tráfico**:  
   - Dentro de `scapy`, ejecutar `sniffer.py` para ver paquetes HTTP reales que pasan por el puerto `8080`.

4. **Pruebas de Fuzzing e Inyección**:  
   - `injector.py` genera:
     - Una petición con URL de 5000 caracteres.
     - Una petición con un método HTTP corrupto (`G€T`).

5. **Pruebas de Modificación**:  
   - `modifier.py` envía:
     - Una solicitud con `Host` inexistente.
     - Un `User-Agent` con caracteres Unicode.
     - Un método `DELETE` sobre `/`.

6. **Visualización externa**:  
   - Se puede usar **Wireshark** en el host para capturar el tráfico (`tcp.port == 8080`).

## 🗂️ Archivos Clave

### `cliente/script.py`
```python
import urllib3
import time

time.sleep(5)
http = urllib3.PoolManager()
response = http.request('GET', 'http://127.0.0.1:8080')
print("Codigo de estado:", response.status)
print("Respuesta:")
print(response.data.decode('utf-8'))
```

### `scapy/sniffer.py`
```python
from scapy.all import *

sniff(iface="any", filter="tcp port 8080", prn=lambda pkt: pkt.show())
```

### `scapy/injector.py`
```python
from scapy.all import *

# Fuzzing 1: URL larga
ip1 = IP(dst="127.0.0.1")
tcp1 = TCP(dport=8080, sport=RandShort(), flags="S")
payload1 = "GET /" + "A"*5000 + " HTTP/1.1\r\nHost: localhost\r\n\r\n"
pkt1 = ip1/tcp1/Raw(load=payload1)
send(pkt1)
print("Inyección 1 enviada")

# Fuzzing 2: Método HTTP con símbolos
ip2 = IP(dst="127.0.0.1")
tcp2 = TCP(dport=8080, sport=RandShort(), flags="S")
payload2 = "G€T / HTTP/1.1\r\nHost: localhost\r\n\r\n"
pkt2 = ip2/tcp2/Raw(load=payload2)
send(pkt2)
print("Inyección 2 enviada")
```

### `scapy/modifier.py`
```python
from scapy.all import *

# Modificación 1: Host inválido
ip1 = IP(dst="127.0.0.1")
tcp1 = TCP(dport=8080, sport=RandShort(), flags="S")
payload1 = "GET / HTTP/1.1\r\nHost: noexiste\r\n\r\n"
pkt1 = ip1/tcp1/Raw(load=payload1)
send(pkt1)
print("Modificación 1 enviada")

# Modificación 2: User-Agent con símbolos
ip2 = IP(dst="127.0.0.1")
tcp2 = TCP(dport=8080, sport=RandShort(), flags="S")
payload2 = "GET / HTTP/1.1\r\nHost: localhost\r\nUser-Agent: 𝔘𝔫𝔦𝔠𝔬𝔡𝔢💥\r\n\r\n"
pkt2 = ip2/tcp2/Raw(load=payload2)
send(pkt2)
print("Modificación 2 enviada")

# Modificación 3: Método DELETE
ip3 = IP(dst="127.0.0.1")
tcp3 = TCP(dport=8080, sport=RandShort(), flags="S")
payload3 = "DELETE / HTTP/1.1\r\nHost: localhost\r\n\r\n"
pkt3 = ip3/tcp3/Raw(load=payload3)
send(pkt3)
print("Modificación 3 enviada")
```

## ✅ Cómo Ejecutar

```bash
sudo docker-compose build
sudo docker-compose up -d
sudo docker exec -it scapy_sniffer bash

# En Scapy:
python sniffer.py

# En otra terminal:
docker exec -it scapy_sniffer bash
python injector.py
python modifier.py

docker logs apache_server (En caso de necesitar ver los logs del servidor)
```

---
⭐️ From [@luvaldev](https://github.com/luvaldev)
