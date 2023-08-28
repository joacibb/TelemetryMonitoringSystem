import socket
import json

def process_tcp_message(message):
    return f"Respuesta simulada del servidor TCP a: {message}"

# Configuración del servidor TCP
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind(('127.0.0.1', 12345))
tcp_server.listen(1)

# Configuración del servidor UDP
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(('127.0.0.1', 54321))

print("Servidores listos para recibir mensajes...")

while True:
    # Aceptar conexiones TCP
    tcp_client, tcp_addr = tcp_server.accept()
    print(f"Conexión TCP establecida desde {tcp_addr}")

    # Recibir mensaje TCP y enviar respuesta simulada
    tcp_message = tcp_client.recv(1024).decode()
    print(f"Mensaje TCP recibido: {tcp_message}")
    tcp_response = process_tcp_message(tcp_message)
    tcp_client.send(tcp_response.encode())
    tcp_client.close()

    # Configurar un tiempo de espera para recibir mensajes UDP
    udp_server.settimeout(1)  # Esperar hasta 1 segundo

    try:
        udp_message, udp_addr = udp_server.recvfrom(1024)
        print(f"Mensaje UDP recibido: {udp_message.decode()} de {udp_addr}")

        # Procesar el mensaje UDP simulado
        try:
            telemetry_data = json.loads(udp_message.decode())
            print("Datos de telemetría recibidos:")
            print(f"Temperatura: {telemetry_data['temperature']:.2f}°C")
            print(f"Humedad: {telemetry_data['humidity']:.2f}%")

            # Enviar respuesta simulada al cliente UDP
            udp_response = "Respuesta simulada del servidor UDP"
            udp_server.sendto(udp_response.encode(), udp_addr)
        except json.JSONDecodeError:
            print("Mensaje UDP no válido")
    except socket.timeout:
        print("No se recibieron mensajes UDP en el tiempo especificado")
