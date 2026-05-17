import subprocess
from config.settings import DEFAULT_TIMEOUT

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