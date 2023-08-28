import socket
import json
import numpy as np
import datetime


def check_server_status():
    try:
        server_address = ('127.0.0.1', 12345)  # Cambia la dirección y el puerto según tu configuración
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client.settimeout(1)  # Establece un tiempo de espera para la conexión

        tcp_client.connect(server_address)
        tcp_client.close()
        return True
    except (socket.error, TimeoutError):
        return False


def send_udp():
    # Verificar el estado del servidor antes de enviar los datos
    if check_server_status():
        udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")

        telemetry_data = {
            "time": current_time,
            "temperature": np.random.uniform(20, 30),
            "humidity": np.random.uniform(40, 60)
        }
        udp_message = json.dumps(telemetry_data)

        udp_client.sendto(udp_message.encode(), ('127.0.0.1', 54321))
        udp_client.close()

        return telemetry_data
    else:
        print("El servidor no está disponible")
        return None
