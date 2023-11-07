import tkinter as tk
from tkinter import messagebox

patients = [
    {"nombre": "Juan", "edad": 30},
    {"nombre": "María", "edad": 25},
]

def add_patient():
    name = name_entry.get()
    age = age_entry.get()
    if name and age:
        patients.append({"nombre": name, "edad": age})
        update_patient_list()
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Por favor, complete todos los campos")

def edit_patient():
    selected_patient = patient_listbox.curselection()
    if selected_patient:
        patient = patients[selected_patient[0]]
        name_entry.delete(0, tk.END)
        name_entry.insert(0, patient["nombre"])
        age_entry.delete(0, tk.END)
        age_entry.insert(0, patient["edad"])

def delete_patient():
    selected_patient = patient_listbox.curselection()
    if selected_patient:
        del patients[selected_patient[0]]
        update_patient_list()

def update_patient_list():
    patient_listbox.delete(0, tk.END)
    for patient in patients:
        patient_listbox.insert(tk.END, f"{patient['nombre']} - {patient['edad']} años")

def get_patient_names():
    return [patient["nombre"] for patient in patients]

def manage_patients(tab_patients):
    global name_entry, age_entry, patient_listbox

    name_label = tk.Label(tab_patients, text="Nombre:")
    name_label.pack()
    name_entry = tk.Entry(tab_patients)
    name_entry.pack()

    age_label = tk.Label(tab_patients, text="Edad:")
    age_label.pack()
    age_entry = tk.Entry(tab_patients)
    age_entry.pack()

    add_button = tk.Button(tab_patients, text="Agregar Paciente", command=add_patient)
    add_button.pack()

    edit_button = tk.Button(tab_patients, text="Editar Paciente Seleccionado", command=edit_patient)
    edit_button.pack()

    delete_button = tk.Button(tab_patients, text="Eliminar Paciente Seleccionado", command=delete_patient)
    delete_button.pack()

    patient_listbox = tk.Listbox(tab_patients)
    patient_listbox.pack(fill=tk.BOTH, expand=1)
    update_patient_list()
