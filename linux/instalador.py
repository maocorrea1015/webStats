import os
from pathlib import Path

SERVICE_NAME = "mi_servicio"
SERVICE_FILE = f"""\
[Unit]
Description=Mi Servicio en Python
After=network.target

[Service]
ExecStart=/usr/local/bin/{SERVICE_NAME}
Restart=always
User=root

[Install]
WantedBy=multi-user.target
"""

def instalar_service():
    service_path = Path(f"/etc/systemd/system/{SERVICE_NAME}.service")
    service_path.write_text(SERVICE_FILE)
    os.system(f"systemctl daemon-reload")
    os.system(f"systemctl enable {SERVICE_NAME}")
    os.system(f"systemctl start {SERVICE_NAME}")
    print(f"Servicio {SERVICE_NAME} instalado y arrancado")

if __name__ == "__main__":
    instalar_service()
