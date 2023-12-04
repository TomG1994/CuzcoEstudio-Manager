from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import Calendar
from ..logic import cargar_datos_reservas
from ..config import get_rutas
from .agenda import AgendaWindow

class CalendarioComp(ttk.Frame):
    def __init__(self, parent, style):
        ttk.Frame.__init__(self, parent)
        self.ruta_base_datos_reservas, _ = get_rutas()
        self.style = style

        # Crear calendario
        self.calendario = Calendar(self, locale='es_ES', showweeknumbers=False)
        self.calendario.pack(fill="both", expand=True)
        self.calendario.bind("<<CalendarSelected>>", self.on_calendar_click)
        self.actualizar_calendario(self.ruta_base_datos_reservas)
        self._last_click_time = 0
        self._click_interval = 500  # Tiempo en milisegundos para considerar un doble clic


    def on_calendar_click(self, event):
        current_time = datetime.now().timestamp() * 1000
        elapsed_time = current_time - self._last_click_time
        self._last_click_time = current_time

        if elapsed_time < self._click_interval:
            self.mostrar_entradas(event, self.style)

    def actualizar_calendario(self, ruta_base_datos_reservas):
        data = cargar_datos_reservas(ruta_base_datos_reservas)

        for event in self.calendario.get_calevents():
            self.calendario.calevent_remove(event)

        self.calendario.tag_config("marcada", background="lightblue")

        for tupla in data:
            fecha_str = tupla[2]
            fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d").date()

            self.calendario.calevent_create(
                fecha_dt,
                f"<span font='Arial 12'>{tupla[0]}</span>\n"
                f"Sala: {tupla[1]}\n"
                f"Fecha: {fecha_dt}\n"
                f"Horario: {tupla[3]}\n"
                f"HR/s: {tupla[4]}\n",
                "marcada",
            )

    def mostrar_entradas(self, event, style):
        selected_date = self.calendario.selection_get()
        if selected_date is not None:
            selected_date_str = selected_date.strftime("%Y-%m-%d")
            data = cargar_datos_reservas(self.ruta_base_datos_reservas)
            entradas_seleccionadas = [tupla for tupla in data if tupla[2] == selected_date_str]

            agenda_window = AgendaWindow(self.master, selected_date, entradas_seleccionadas, style, self.ruta_base_datos_reservas)
            agenda_window.geometry("600x400")
            self.after(100, agenda_window.aplicar_grab_set)