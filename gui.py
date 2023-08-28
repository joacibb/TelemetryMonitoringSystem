import threading
import tkinter as tk
import socket
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import csv

from clientTCP import send_tcp
from clientUDP import send_udp

CSV_FILE_PATH = "telemetry_data.csv"


def on_exit():
    root.destroy()


def save_to_csv(telemetry_data):
    with open(CSV_FILE_PATH, "a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([telemetry_data["time"], telemetry_data["temperature"], telemetry_data["humidity"]])


def check_server_status():
    server_address = "127.0.0.1"
    server_port = 12345

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    try:
        sock.connect((server_address, server_port))
        sock.close()
        return "Online"
    except socket.error:
        return "Offline"


class TelemetryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Telemetry GUI")
        self.root.geometry("1360x900")

        self.status_frame = tk.Frame(root, bg="white")
        self.status_frame.pack(side="top", anchor="ne", padx=10, pady=10)

        self.tcp_button = tk.Button(root, text="Enviar por TCP", command=self.send_tcp)
        self.tcp_button.pack()

        self.udp_button = tk.Button(root, text="Enviar por UDP", command=self.send_udp)
        self.udp_button.pack()

        self.status_label = tk.Label(self.status_frame, text="Estado: Desconectado", font=("Helvetica", 12), fg="white")
        self.status_label.pack()

        self.telemetry_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.telemetry_label.pack()

        self.fig, self.ax = plt.subplots(figsize=(15, 15))
        self.temperature_data = []
        self.time_data = []
        self.time_labels = []
        self.time_counter = 0
        self.line, = self.ax.plot(self.time_data, self.temperature_data, label="Temperatura (°C)")
        self.ax.set_xlabel("Hora")
        self.ax.set_ylabel("Temperatura (°C)")
        self.ax.legend()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        self.ani = FuncAnimation(self.fig, self.update_graph, interval=1000, save_count=10)

        self.status_check_thread = threading.Thread(target=self.check_server_status_periodically)
        self.status_check_thread.daemon = True
        self.status_check_thread.start()

    def check_server_status_periodically(self):
        self.update_server_status()
        self.root.after(60000, self.check_server_status_periodically)  # 60000 ms = 1 minuto

    def update_server_status(self):
        status = check_server_status()
        self.status_label.config(text=f"Status: {status}")
        self.status_label.config(bg="green" if status == "Online" else "red")

    def update_graph(self, frame):
        self.line.set_xdata(self.time_data)
        self.line.set_ydata(self.temperature_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

    def send_tcp(self):
        tcp_message = "Mensaje simulado al servidor TCP"
        tcp_response = send_tcp(tcp_message)
        self.telemetry_label.config(text=tcp_response)

    def send_udp(self):
        telemetry_data = send_udp()

        if telemetry_data is not None:
            self.temperature_data.append(telemetry_data["temperature"])
            self.time_labels.append(telemetry_data["time"])
            self.time_data.append(self.time_counter)
            self.time_counter += 1
            self.ax.set_xticks(self.time_data)
            self.ax.set_xticklabels(self.time_labels, rotation=45)
            self.canvas.draw()

            save_to_csv(telemetry_data)


if __name__ == "__main__":
    root = tk.Tk()
    app = TelemetryApp(root)
    root.protocol("WM_DELETE_WINDOW", on_exit)
    root.after(0, app.update_server_status)  # Update status immediately
    root.mainloop()
