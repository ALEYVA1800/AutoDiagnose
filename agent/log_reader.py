import os
import subprocess
from config.settings import BASE_LOG_DIR, DEFAULT_TIMEOUT

def read_system_logs(logname: str, lines: int = 30) -> str:
    """
    Lee las ultimas lineas de un archivo de log específico dentro de /var/log/
    Args:
        log_name: Nombre del archivo relativo a /var/log/ (ej. 'syslog', 'auth.log').
        lines: Cantidad de líneas finales a leer.
    """
    target_path = os.path.abspath(os.path.join(BASE_LOG_DIR,logname))

    # Verifica que exista el archivo y se tenga acceso
    if not target_path.startswith(BASE_LOG_DIR):
        return "Error de seguridad: Acceso denegado fuera de /var/log"
    
    if not os.path.exists(target_path):
        return f"El archivo de log '{logname}' no existe en {BASE_LOG_DIR}"
    
    try:
        result = subprocess.run(['tail','-n',str(lines),target_path],
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True, 
                                timeout=DEFAULT_TIMEOUT)
        
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Error al leer archivo de log: {str(e)}"
