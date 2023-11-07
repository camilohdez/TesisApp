import tkinter as tk
from tkinter import ttk
from graphs import show_graphs
from patients import manage_patients
from patients import manage_patients, get_patient_names
from graphs import show_graphs

def main_window():
    window = tk.Tk()
    window.title("Sistema de Sensores Inerciales")

    # Crear pestañas para diferentes secciones
    tab_control = ttk.Notebook(window)
    
    # Pestaña de Gráficas
    tab_graphs = ttk.Frame(tab_control)
    tab_control.add(tab_graphs, text="Gráficas")
    show_graphs(tab_graphs, get_patient_names()) # Pasa la lista de pacientes aquí

    # Pestaña de Gestión de Pacientes
    tab_patients = ttk.Frame(tab_control)
    tab_control.add(tab_patients, text="Pacientes")
    manage_patients(tab_patients)

    tab_control.pack(expand=1, fill="both")

    window.mainloop()
