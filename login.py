import tkinter as tk
from main_window import main_window

def authenticate(username, password):
    # Aquí puedes agregar la lógica de autenticación real, como verificar en una base de datos.
    # Por ahora, solo estamos haciendo una comprobación simple.
    return username == "admin" and password == "password"

def login():
    username = username_entry.get()
    password = password_entry.get()
    if authenticate(username, password):
        login_window.destroy()
        main_window()
    else:
        error_label.config(text="Usuario o contraseña incorrectos")

login_window = tk.Tk()
login_window.title("Iniciar Sesión")

username_label = tk.Label(login_window, text="Usuario:")
username_label.pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

password_label = tk.Label(login_window, text="Contraseña:")
password_label.pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

login_button = tk.Button(login_window, text="Iniciar Sesión", command=login)
login_button.pack()

error_label = tk.Label(login_window, text="", fg="red")
error_label.pack()

login_window.mainloop()
