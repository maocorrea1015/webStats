#!/usr/bin/env python3
import psutil
import platform
import socket
import time
import requests
import logging

# === Configuración ===
API_URL = "https://tuservidor.com/api/metrics"  # URL de tu API
API_KEY = "TU_API_KEY"  # Token para autenticar
INTERVALO = 5  # Segundos entre envíos

# === Configuración de logs ===
logging.basicConfig(
    filename="/var/log/mi_servicio.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === Funciones ===
def get_system_info():
    return {
        "hostname": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname()),
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor()
    }

def get_resource_usage():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_used_mb": round(psutil.virtual_memory().used / (1024 ** 2), 2),
        "ram_total_mb": round(psutil.virtual_memory().total / (1024 ** 2), 2),
        "disk_percent": psutil.disk_usage('/').percent
    }

def get_network_usage(prev_net):
    net = psutil.net_io_counters()
    bytes_sent = net.bytes_sent - prev_net.bytes_sent
    bytes_recv = net.bytes_recv - prev_net.bytes_recv
    return bytes_sent, bytes_recv, net

def send_metrics(data):
    try:
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        r = requests.post(API_URL, json=data, headers=headers, timeout=5)
        if r.status_code != 200:
            logging.error(f"Error enviando datos: {r.status_code} - {r.text}")
    except Exception as e:
        logging.error(f"Error de conexión: {e}")

# === Función principal ===
def main():
    logging.info("Servicio iniciado: enviando métricas cada %s segundos", INTERVALO)
    system_info = get_system_info()
    prev_net = psutil.net_io_counters()

    try:
        while True:
            resources = get_resource_usage()
            sent, recv, prev_net = get_network_usage(prev_net)

            payload = {
                **system_info,
                **resources,
                "net_sent_kb": round(sent / 1024, 2),
                "net_recv_kb": round(recv / 1024, 2),
                "timestamp": time.time()
            }

            send_metrics(payload)
            logging.info("Métricas enviadas: %s", payload)
            time.sleep(INTERVALO)

    except KeyboardInterrupt:
        logging.info("Servicio detenido manualmente")
    except Exception as e:
        logging.error(f"Error en el servicio: {e}")

# === Ejecución ===
if __name__ == "__main__":
    main()
