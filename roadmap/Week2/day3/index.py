

import re

patron = r"Failed password for .* from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
intentos_por_ip = {}

with open("auth.log") as authLog:
  for linea in authLog:
    coincidencia = re.search(patron, linea)
    if coincidencia:
      ip = coincidencia.group(1) 
      if ip in intentos_por_ip:
          intentos_por_ip[ip] += 1
      else:
        intentos_por_ip[ip] = 1

print("IPs sospechosas detectadas:")
for ip, conteo in intentos_por_ip.items():
  print(f"{ip}: {conteo} intentos de acceso fallidos")