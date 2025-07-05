import urllib3
import time

time.sleep(5)

http = urllib3.PoolManager()
response = http.request('GET', 'http://servidor:80')
http.request('GET', 'http://servidor/index.html')
print("Codigo de estado:", response.status)
print("Respuesta:")
print(response.data.decode('utf-8'))

