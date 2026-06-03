### 🔑 Event ID 4624: Inicio de Sesión Exitoso Anómalo
* **Técnica MITRE ATT&CK:** T1078 (Valid Accounts) / T1550.002 (Pass the Hash)
* **Evidencia:** Se detectó un inicio de sesión de red (Logon Type 3) para el usuario
 `Administrator` utilizando el protocolo `Kerberos`, donde la IP de origen es la
  interfaz local `127.0.0.1`. Esto sugiere una suplantación de identidad o inyección de
   credenciales local (Overpass-the-Hash).