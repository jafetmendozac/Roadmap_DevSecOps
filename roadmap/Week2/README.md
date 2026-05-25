# Análisis de Telemetría: Protocolo SMBv1 (Puerto 445)

## 1. Metodología del Entorno
- **Origen de los datos:** Análisis de tráfico de red mediante un archivo de captura pública (`.pcapng`).
- **Herramienta utilizada:** Wireshark v4.x.
- **Filtro aplicado:** `smb` (Aislamiento de la versión antigua SMBv1).

## 2. Hallazgos en el Análisis de Tráfico
Tras analizar la fase de negociación (`Negotiate Protocol`) y la autenticación exitosa (`Session Setup AndX Response` con estatus `STATUS_SUCCESS`), se identificó la solicitud explícita del cliente para montar un recurso compartido en la red.

### Paquete bajo inspección: Tree Connect AndX Request
- **Protocolo / OpCode:** SMBv1 / Tree Connect AndX (0x75)
- **Servidor Objetivo:** `192.168.199.134`
- **Recurso Solicitado (Path):** `\\192.168.199.134\STUFF`

> **Nota de Ingeniería Defensiva:** El campo `Path` dentro del comando `0x75` revela que el cliente apuntó a un recurso compartido personalizado llamado `STUFF`. Al no ser un recurso administrativo estándar (como `IPC$`), este tipo de shares requiere un monitoreo estricto de auditoría de acceso a objetos para prevenir la exfiltración de información sensible corporativa.