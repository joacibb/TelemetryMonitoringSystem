import socket

def send_tcp(message):
    try:
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client.connect(('127.0.0.1', 12345))

        tcp_client.send(message.encode())

        # Establecer un tiempo de espera de 5 segundos para la recepción de datos
        tcp_client.settimeout(5)
        tcp_response = tcp_client.recv(1024).decode()
        tcp_client.close()

        return tcp_response
    except socket.error as e:
        return f"Socket error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"
