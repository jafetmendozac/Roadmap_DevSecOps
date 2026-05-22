# Network Telemetry Parsing - Semana 1

## Objetivos de la Semana
- Describir cómo se estructuran los paquetes IP, el handshake TCP y las consultas DNS.
- Utilizar Wireshark para capturar y filtrar tráfico real, identificando las capas de los paquetes.
- Explicar cómo los atacantes abusan del DNS para Comando y Control (C2).
- Construir un script básico en Node.js que te permita "ver" el tráfico HTTP en bruto

## Notas de Análisis de Paquetes
*   **TCP Handshake**: El paquete con flag SYN inicia la conexión. Para verlos: `tcp.flags.syn == 1`.
*   **DNS Query**: Una consulta típica es `dns.qry.name`. Un patrón anómalo serían subdominios muy largos o con caracteres extraños.
*   **HTTP**: Los métodos y rutas están en la primera línea de la petición.

## Expresiones Regulares para Anomalías
*   **Detectar posible DNS Tunneling (subdominio largo)**: `dns.qry.name matches "[a-zA-Z0-9]{20,}\."`
*   **Detectar User-Agent inusual (muy corto o vacío)**: `http.user_agent matches "^$|^ {0,5}$"`

## Código: Servidor TCP con Parser HTTP
[Pega aquí el código de tu `server.js` final]

## Demostración
[Incluye un screenshot de tu consola mostrando el servidor recibiendo una petición curl y parseándola]