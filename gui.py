import tkinter as tk
import socket
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np
import datetime
import csv

from clientTCP import send_tcp
from clientUDP import send_udp

CSV_FILE_PATH = "telemetry_data.csv"


def on_exit():
    root.destroy()  # Cierra la ventana antes de salir


def save_to_csv(telemetry_data):
    with open(CSV_FILE_PATH, "a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([telemetry_data["time"], telemetry_data["temperature"], telemetry_data["humidity"]])


class TelemetryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Telemetry GUI")
        self.root.geometry("1360x900")

        self.tcp_button = tk.Button(root, text="Enviar por TCP", command=self.send_tcp)
        self.tcp_button.pack()

        self.udp_button = tk.Button(root, text="Enviar por UDP", command=self.send_udp)
        self.udp_button.pack()

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
    root.protocol("WM_DELETE_WINDOW", on_exit)  # Asocia on_exit al evento de cierre de ventana
    root.mainloop()
