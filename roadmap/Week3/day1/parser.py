import json
from evtx import PyEvtxParser

def parse_evtx_to_normalized_json(evtx_path, output_path):
    """
    Parser de EVTX a JSON normalizado optimizado para incidentes reales (KrbRelayUp, Shims, etc.)
    """
    parser = PyEvtxParser(evtx_path)
    normalized_logs = []
    
    for record in parser.records_json():
        event_data = json.loads(record['data'])
        event = event_data.get('Event', {})
        system = event.get('System', {})
        
        # Obtener y asegurar que el ID sea un ENTERO
        event_id_raw = system.get('EventID', 0)
        if isinstance(event_id_raw, dict):
            event_id = int(event_id_raw.get('#text', 0))
        else:
            event_id = int(event_id_raw)
            
        # Estructura Base Normalizada
        normalized_entry = {
            "timestamp": system.get('TimeCreated', {}).get('@SystemTime'),
            "computer": system.get('Computer'),
            "event_id": event_id,
            "task": system.get('Task'),
            "level": system.get('Level'),
            "logon_type": None,
            "target_user": None,
            "process_path": None,
            "service_name": None,
            "service_path": None,
            "raw_data": event.get('EventData', {}) 
        }
        
        # --- CORRECCIÓN 1: Extraer data_dict directamente ---
        event_data_section = event.get('EventData', {})
        data_dict = {}
        
        if isinstance(event_data_section, dict):
            # Clonamos el diccionario directo que provee PyEvtxParser
            data_dict = event_data_section.copy()
            # Fallback en caso de que use formato anidado de listas antiguas
            if 'Data' in event_data_section and isinstance(event_data_section['Data'], list):
                for item in event_data_section['Data']:
                    if isinstance(item, dict):
                        data_dict[item.get('@Name')] = item.get('#text')
        
        # --- CORRECCIÓN 2: Validaciones homogéneas usando Enteros (int) ---
        if event_id == 4624:
            normalized_entry["task"] = "Successful Logon Detected"
            normalized_entry["logon_type"] = data_dict.get('LogonType')
            normalized_entry["target_user"] = data_dict.get('TargetUserName')
            normalized_entry["process_path"] = data_dict.get('IpAddress')
        
        elif event_id == 4688:
            normalized_entry["task"] = "Process Creation Detected"
            normalized_entry["target_user"] = data_dict.get('SubjectUserName')
            normalized_entry["process_path"] = data_dict.get('NewProcessName')
            normalized_entry["command_line"] = data_dict.get('CommandLine')
        
        elif event_id == 7045:
            normalized_entry["task"] = "New Service Installed"
            normalized_entry["service_name"] = data_dict.get('ServiceName')
            normalized_entry["service_path"] = data_dict.get('ImagePath')
        
        elif event_id == 500:
            normalized_entry["task"] = "Application Shim Execution Detected"
            normalized_entry["process_path"] = data_dict.get('ProgramName') or data_dict.get('ExeName') or "Ver Raw Data"
            normalized_entry["command_line"] = data_dict.get('ProgramId') or "Mecanismo Shim Activado"

        normalized_logs.append(normalized_entry)
    
    # Guardar resultados
    with open(output_path, 'w') as f:
        json.dump(normalized_logs, f, indent=2)
    
    print(f"✅ Parseados {len(normalized_logs)} eventos críticos en {output_path}")

# Ejecución dirigida a tu muestra de Escalada de Privilegios
if __name__ == "__main__":
    parse_evtx_to_normalized_json(
        "EVTX-ATTACK-SAMPLES/Privilege Escalation/privesc_KrbRelayUp_windows_4624.evtx",
        "normalized_alerts.json"
    )