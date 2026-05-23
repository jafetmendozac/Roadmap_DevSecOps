# Network Telemetry Parsing - Semana 1

## Objetivos de la Semana
- Describir cómo se estructuran los paquetes IP, el handshake TCP y las consultas DNS.
- Utilizar Wireshark para capturar y filtrar tráfico real, identificando las capas de los paquetes.
- Explicar cómo los atacantes abusan del DNS para Comando y Control (C2).
- Construir un script básico en Node.js que te permita "ver" el tráfico HTTP en bruto

## Notas de Análisis de Paquetes
*   **Start my server**: Usamos el comando `tcp.port == 3000` para ver unicamente el trafico que paso por nuestro servidor y en tu terminal  .
*   **TCP Handshake**: El paquete con flag SYN inicia la conexión. Para verlos: `tcp.flags.syn == 1`.
  - SYN (Synchronize): El cliente le dice al servidor "Quiero iniciar una conexión".
  - SYN-ACK (Synchronize-Acknowledgment): El servidor responde "Recibido, yo también   estoy listo".
  - ACK (Acknowledgment): El cliente confirma "¡Entendido, empecemos!".
*   **DNS Query**: Una consulta típica es `dns.qry.name`. Un patrón anómalo serían subdominios muy largos o con caracteres extraños.
*   **HTTP**: Los métodos y rutas están en la primera línea de la petición.

## Explicación del Abuso del protocolo DNS para Comando Y Control (C2)
Los atacante saben que ninguna empresa va a bloquear este protocolo DNS(puerto 53) porque perderían por completo la conectividad a internet  entonces aprovechan esta confianza para hacer pequeñas consultas, ocultar comandos o datos robados ya que aunque haya el Firewall es complicado que lo detecto ya que este no lo analiza a profundidad todos los paquetes que se mandan por la red.A esto se le conoce como un canal de baja y lenta velocidad(low-and-slow).

### Servidor TCP con Parser HTTP 💻
Para correr el servidor desde la terminal de tu IDE, ubícate en: `cd roadmap/Week1` y luego levántalo con `node server.js`. Puedes probar su funcionamiento ejecutando:
```bash
curl http://localhost:3000/contactos
```
## Validación de Seguridad (Regex) 🔒:
-  El servidor incluye una regla de inspección mediante expresiones regulares para analizar el encabezado `User-Agent`. Esto permite identificar y bloquear peticiones anómalas, como herramientas de escaneo automatizadas o cadenas con longitudes inusuales antes de que interactúen con la lógica interna.
  **Validación de Seguridad y Mitigación 🧪**
  Para comprobar el correcto funcionamiento de nuestro sistema de prevención de intrusos básico, realizamos una prueba de concepto (PoC) enviando un encabezado anómalo:
  ```bash
  curl http://localhost:3000/contactos -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ajdf;oakkldf'asjfkj'asdkfj'
  ```
  - Resultado en el Servidor 🖥️: El parser detecta que la longitud de la cadena del User-Agent supera el límite permitido por la expresión regular. Imprime la alerta Warning: User-Agent is too long y ejecuta socket.destroy().

  - Resultado en el Cliente 🛑: La herramienta curl reporta el error curl: (52) Empty reply from server. Esto confirma que la conexión se interrumpió de inmediato mediante un paquete RST, evitando el desperdicio de recursos del servidor o el procesamiento de datos maliciosos.

  Nota: socket.end() termina el proceso de manera amistosa(deja que los procesos se terminen)
## Demostración
En las carpeta assets hay imagenes acerca del tcp Handshake en Wireshark