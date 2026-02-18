import flet as ft
import matplotlib.pyplot as plt
import numpy as np
# BLOQUE 1: Unión de Sistemas y Civil
# Esta es la pieza que permite meter el dibujo de la parábola en la ventana
from flet.matplotlib_chart import MatplotlibChart

def main(page: ft.Page):
    # BLOQUE 2: Configuración de la Ventana (Sistemas)
    page.title = "Asistente Estructural - Jhulian"
    page.window_width = 450
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT

    # BLOQUE 3: Entradas de datos (Ingeniería Civil)
    txt_luz = ft.TextField(label="Longitud de la viga (m)", border_radius=10)
    txt_carga = ft.TextField(label="Carga distribuida (kg/m)", border_radius=10)
    lbl_res = ft.Text("Resultado: Mmax = 0.00 kg-m", size=20, weight="bold")
    
    # Espacio donde aparecerá el dibujo
    grafico_placeholder = ft.Column()

    # BLOQUE 4: El Cerebro (Lógica de cálculo)
    def calcular_click(e):
        # Convertimos texto a números
        L = float(txt_luz.value)
        W = float(txt_carga.value)
        
        # Fórmulas de ingeniería
        m_max = (W * L**2) / 8
        lbl_res.value = f"Resultado: Mmax = {m_max:.2f} kg-m"

        # Crear el gráfico
        fig, ax = plt.subplots()
        x = np.linspace(0, L, 100)
        y = ((W * L) / 2 * x) - (W * x**2) / 2
        ax.plot(x, y, color='red')
        ax.invert_yaxis() # Momentos positivos hacia abajo
        
        # Meter el gráfico en la ventana
        grafico_placeholder.controls.clear()
        grafico_placeholder.controls.append(MatplotlibChart(fig, expand=True))
        page.update()

    # BLOQUE 5: Armado de la pantalla
    btn = ft.ElevatedButton("Calcular Momento Máximo", on_click=calcular_click)
    page.add(
        ft.Text("Software de Jhulian", size=30, weight="bold"),
        txt_luz, 
        txt_carga, 
        btn, 
        lbl_res,
        grafico_placeholder
    )

# BLOQUE 6: Encendido
if __name__ == "__main__":
    ft.app(target=main)