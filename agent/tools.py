import subprocess
import platform
from config.settings import DEFAULT_TIMEOUT
from agent.log_reader import read_system_logs

TOOLS_LIST = []

def tool(func):
    TOOLS_LIST.append(func)
    return func

tool(read_system_logs)

def get_os_context()-> str:
    """
    Detecta el sistema operativo y la distro para proveer contexto al modelo
    """
    sys_type = platform.system()

    if sys_type == "Linux":
        try:
            os_info = platform.freedesktop_os_release()
            distro_name = os_info.get("NAME","Linux")
            version = os_info.get("VERSION_ID","Desconocida")
            return f"Linux (Distro: {distro_name}, Ver.:{version} ({platform.machine()})"
        except AttributeError:
            return f"Linux (Kernel: {platform.release()}, Arquitectura: {platform.machine()} )"
    elif sys_type == "Darwin":
        return f"macOS (Version: {platform.mac_ver()[0]}, Arquitectura: {platform.machine()})"
    
    return f"{sys_type} (Version: {platform.release()}, Arquitectura: {platform.machine()})"

@tool
def list_active_services() -> str:
    """
    Obtiene una lista compacta de todos los servicios de systemd que están activos y corriendo.
    """

    try:
        result = subprocess.run(['systemctl','list-units','--type=service','--state=running', '--no-legend','--no-pager'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                timeout=DEFAULT_TIMEOUT)
        return result.stdout if result.stdout else "No se detectaron servicios activos"
    except Exception as e:
        return f"Error al listar los servicios de systemd: {str(e)}"

@tool
def check_systemd_status(service_name: str) -> str:
    """Obtiene el estado actual de un servicio de systemd (systemctl status)."""
    try:
        result = subprocess.run(
            ["systemctl","status",service_name],
            stdout  = subprocess.PIPE,
            stderr  = subprocess.PIPE,
            text    = True,
            timeout = DEFAULT_TIMEOUT
        )

        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Error en systemctl status: {str(e)}"

@tool
def get_journalctl_logs(service_name: str, lines: int = 20) -> str:
    """Obtiene las últimas líneas de log de un servicio específico usando journalctl."""
    try:
        result = subprocess.run(
            ['journalctl', '-u', service_name, '-n', str(lines), '--no-pager'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=DEFAULT_TIMEOUT
        )
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Error en journalctl: {str(e)}"

@tool
def check_network_interfaces() -> str:
    """Obtiene la configuración actual de las interfaces de red y sus direcciones IP (ip a)."""
    try:
        result = subprocess.run(
            ['ip', 'a'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=DEFAULT_TIMEOUT
        )
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Error al verificar interfaces: {str(e)}"

@tool
def search_installed_services(keyword: str) -> str:
    """
    Busca archivos de servicio instalados en el sistema (en disco) que coincidan 
    con una palabra clave, incluso si no están cargados en memoria.
    Args:
        keyword: Palabra clave o nombre parcial del servicio a buscar (ej. 'ufw', 'firewall', 'nginx').
    """
    # Sanitización básica para evitar inyección de caracteres raros en el comando
    clean_keyword = "".join(c for c in keyword if c.isalnum() or c in ['-', '_', '*'])
    
    # Si el usuario no puso comodines, los ponemos nosotros alrededor para buscar coincidencias parciales
    if "*" not in clean_keyword:
        query = f"*{clean_keyword}*"
    else:
        query = clean_keyword

    try:
        # Ejecutamos list-unit-files filtrando por el patrón del servicio
        result = subprocess.run(
            ['systemctl', 'list-unit-files', query, '--type=service', '--no-legend', '--no-pager'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=DEFAULT_TIMEOUT
        )
        
        output = result.stdout.strip()
        return output if output else f"No se encontró ningún servicio instalado que coincida con '{keyword}'."
        
    except Exception as e:
        return f"Error al buscar archivos de servicio: {str(e)}"    