# Análisis de Autenticación Corporativa: Kerberos (Puerto 88)

## 1. Metodología y Telemetría del Entorno
- **Dominio Analizado (Realm):** `CDOM.ACME.COM`
- **Host Cliente (Origen):** `192.168.47.222` (`IEWIN7C`)
- **Controlador de Dominio (KDC - Destino):** `192.168.47.110`

## 2. Correlación Forense de Paquetes (Handshake)

### Paso 1: Solicitud de Autenticación (Frame 7 - AS-REQ)
El cliente inicia una solicitud de autenticación para la entidad (cname) `nava@cdom.acme.com`. En esta fase defensiva preliminar, se observa que el cliente ofrece capacidades criptográficas heredadas como `eTYPE-ARCFOUR-HMAC-MD5 (23)` (RC4), además de los estándares modernos de AES.

### Paso 2: Mecanismo de Control del KDC (Frame 8 - KRB-ERROR)
El Controlador de Dominio intercepta la solicitud inicial y responde inmediatamente con un paquete de control de tipo `KRB-ERROR`.

- **Análisis del Error:** Tras la disección del paquete, se identificó el código de error `KRB5KDC_ERR_PREAUTH_REQUIRED (25)`.
- **Interpretación de Seguridad:** Este comportamiento confirma que el Active Directory tiene **habilitada la Pre-autenticación obligatoria** para la cuenta de usuario `nava`. Esto invalida la posibilidad de ejecutar un ataque directo de *AS-REP Roasting* offline, ya que el KDC se niega a emitir un ticket cifrado sin una prueba de identidad previa basada en el hash de la contraseña.

## 3. Conclusión Defensiva
La infraestructura demuestra una postura segura por defecto ante vectores de ataque de extracción de hashes en la fase de AS-REQ. Se recomienda auditar que todas las cuentas del dominio sigan manteniendo la política de pre-autenticación activa.