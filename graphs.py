import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import paho.mqtt.client as mqtt
import json

# Variables globales
sampling = False
axes_per_sensor = [[None, None] for _ in range(7)]  # Dos gráficas por sensor
sensor_data = [[[0, 0, 0, 0, 0, 0] for _ in range(2)] for _ in range(7)]  # Datos iniciales para 7 sensores
canvas_per_sensor = [None for _ in range(7)]  # Un canvas para cada sensor

# Configuración del cliente MQTT
mqtt_broker = "192.168.0.3"
mqtt_port = 1883
mqtt_topic = "datos/sensor1"

# Función para actualizar los datos del sensor
def on_message(client, userdata, message):
    global sensor_data
    try:
        payload = json.loads(message.payload.decode())
        sensor_index = payload["sensor_index"]
        # Añadir nuevos datos en lugar de reemplazarlos
        #print(f"Datos recibidos para el sensor {sensor_index}: {payload}")
        sensor_data[sensor_index][0].append((payload["ax_m_s2"], payload["ay_m_s2"], payload["az_m_s2"]))
        sensor_data[sensor_index][1].append((payload["gyro_x"], payload["gyro_y"], payload["gyro_z"]))

        # Opcional: Limitar el tamaño de los datos para evitar un consumo excesivo de memoria
        if len(sensor_data[sensor_index][0]) > 100:  # Mantener solo los últimos 100 puntos
            sensor_data[sensor_index][0].pop(0)
        if len(sensor_data[sensor_index][1]) > 100:
            sensor_data[sensor_index][1].pop(0)

    except Exception as e:
        print(f"Error al procesar los datos recibidos: {e}")

# Configuración del cliente MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)
client.subscribe(mqtt_topic)
client.loop_start()

def update_graph():
    global sampling
    if sampling:
        for i, sensor_axes in enumerate(axes_per_sensor):
            if sensor_axes[0] and sensor_axes[1] and canvas_per_sensor[i]:
                sensor_axes[0].clear()
                sensor_axes[1].clear()

                # Verificar si hay datos suficientes antes de desempaquetar
                if sensor_data[i][0] and isinstance(sensor_data[i][0][0], (list, tuple)) and len(sensor_data[i][0][0]) == 3:
                    ax_data, ay_data, az_data = zip(*sensor_data[i][0])
                    sensor_axes[0].plot(ax_data, label="ax")
                    sensor_axes[0].plot(ay_data, label="ay")
                    sensor_axes[0].plot(az_data, label="az")
                    sensor_axes[0].set_title(f"Sensor {i + 1}, Aceleración")
                    sensor_axes[0].legend()

                if sensor_data[i][1] and isinstance(sensor_data[i][1][0], (list, tuple)) and len(sensor_data[i][1][0]) == 3:
                    gyro_x_data, gyro_y_data, gyro_z_data = zip(*sensor_data[i][1])
                    sensor_axes[1].plot(gyro_x_data, label="gyro_x")
                    sensor_axes[1].plot(gyro_y_data, label="gyro_y")
                    sensor_axes[1].plot(gyro_z_data, label="gyro_z")
                    sensor_axes[1].set_title(f"Sensor {i + 1}, Giroscopio")
                    sensor_axes[1].legend()

                canvas_per_sensor[i].draw()
    root.after(1000, update_graph)




def start_sampling():
    global sampling
    sampling = True

def pause_sampling():
    global sampling
    sampling = False

def generate_pdf():
    # Aquí va la lógica para generar el PDF
    pass

def show_sensor_graphs(sensor_index):
    global axes_per_sensor, canvas_per_sensor, tab_graphs
    # Limpiar gráficas anteriores
    for widget in tab_graphs.winfo_children():
        widget.destroy()

    # Datos de prueba
    test_data = [i for i in range(100)]

    # Crear gráficas para el sensor seleccionado
    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(test_data, label="Test Data")
    ax1.set_title(f"Sensor {sensor_index + 1}, Test Aceleración")
    ax1.legend()

    ax2.plot(test_data, label="Test Data")
    ax2.set_title(f"Sensor {sensor_index + 1}, Test Giroscopio")
    ax2.legend()

    axes_per_sensor[sensor_index] = [ax1, ax2]

    # Mostrar la gráfica en la interfaz
    canvas = FigureCanvasTkAgg(fig, master=tab_graphs)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas_per_sensor[sensor_index] = canvas


# Crear la ventana principal
root = tk.Tk()
root.title("Monitor de Sensores")

# Crear un frame para los botones de control
control_frame = tk.Frame(root)
control_frame.pack(side=tk.TOP, fill=tk.X)

# Botones de control
start_button = tk.Button(control_frame, text="Iniciar Muestreo", command=start_sampling)
start_button.pack(side=tk.LEFT)

pause_button = tk.Button(control_frame, text="Pausar Muestreo", command=pause_sampling)
pause_button.pack(side=tk.LEFT)

report_button = tk.Button(control_frame, text="Generar Informe PDF", command=generate_pdf)
report_button.pack(side=tk.LEFT)

# Crear el tablero de gráficas
tab_control = ttk.Notebook(root)
tab_control.pack(expand=1, fill="both")

# Crear la pestaña de gráficas
tab_graphs = ttk.Frame(tab_control)
tab_control.add(tab_graphs, text="Gráficas")

# Botones para cada sensor
for i in range(7):
    sensor_button = tk.Button(tab_graphs, text=f"Sensor {i + 1}", command=lambda i=i: show_sensor_graphs(i))
    sensor_button.pack()

# Iniciar actualización de gráficas
update_graph()

# Inicializar la lista de ejes para cada sensor
axes_per_sensor = [[None, None] for _ in range(7)]

# Ejecutar la aplicación
root.mainloop()




