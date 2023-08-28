import random


def generate_sensor_data():
    temperature = random.uniform(20, 30)  # Simula temperatura entre 20°C y 30°C
    humidity = random.uniform(40, 60)  # Simula humedad entre 40% y 60%
    return temperature, humidity


# Simulamos generación de datos cada segundo
while True:
    temperature, humidity = generate_sensor_data()
    print(f"Temperatura: {temperature:.2f}°C, Humedad: {humidity:.2f}%")
