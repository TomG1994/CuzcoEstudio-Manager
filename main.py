import os

import sys
sys.path.append('../components/')

from components.gui.calendar import CalendarioComp
from components.logic import crear_tabla_reservas, crear_bandas_db
from components.config import set_rutas

import tkinter as tk
from tkinter import ttk

def change_view(event):
    selected_tab = notebook.index(notebook.select())

calendario_comp = CalendarioComp

# Crear la ventana principal
root = tk.Tk()
root.geometry("750x500")
root.title('CuzcoManager')

style = ttk.Style(root)

current_directory = os.path.dirname(os.path.abspath(__file__))
root.tk.call("source", (os.path.join(current_directory, "styles", "forest-dark.tcl")))
root.tk.call("source", (os.path.join(current_directory, "styles", "forest-light.tcl")))

style.theme_use("forest-light")

ruta_carpeta_data = os.path.join(current_directory, 'components', 'data')
if not os.path.exists(ruta_carpeta_data):
    os.makedirs(ruta_carpeta_data)

ruta_base_datos_reservas = os.path.join(ruta_carpeta_data, 'calendario_reservas.db')
ruta_base_datos_bandas = os.path.join(ruta_carpeta_data, 'bandas_info.db')

set_rutas(ruta_base_datos_reservas, ruta_base_datos_bandas)

crear_tabla_reservas(ruta_base_datos_reservas)
crear_bandas_db(ruta_base_datos_bandas)

notebook = ttk.Notebook(root)

calendario_frame = ttk.Frame(notebook)
bar_frame = tk.Frame(notebook)
expensas_frame = ttk.Frame(notebook)

notebook.add(calendario_frame, text='Calendario')
notebook.add(bar_frame, text='Bar')
notebook.add(expensas_frame, text='Expensas')

notebook.pack(fill='both', expand=True)

notebook.bind("<<NotebookTabChanged>>", change_view)

calendario_frame_content = calendario_comp(calendario_frame, style)
calendario_frame_content.pack(fill="both", expand=True)

root.mainloop()