import matplotlib.pyplot as plt
import numpy as np

def calcular_viga_visual():
    print("--- APP ESTRUCTURAL: DIAGRAMA DE MOMENTOS ---")
    try:
        # 1. Datos de entrada
        luz_str = input("Longitud de la viga (m): ")
        carga_str = input("Carga distribuida w (kg/m): ")
        
        L = float(luz_str)
        W = float(carga_str)

        # 2. Cálculos de ingeniería
        R = (W * L) / 2
        M_max = (W * L**2) / 8

        # 3. Generar puntos para la parábola
        x = np.linspace(0, L, 100)
        momentos = (R * x) - (W * x**2) / 2

        # 4. Dibujo técnico
        plt.figure(figsize=(10, 5))
        plt.plot(x, momentos, color='red', linewidth=2, label='Momento Flector (M)')
        plt.fill_between(x, momentos, color='red', alpha=0.2)
        
        # Convención estructural: momentos positivos abajo
        plt.gca().invert_yaxis() 
        
        plt.title(f"Diagrama de Momento Flector (Mmax = {M_max:.2f} kg-m)")
        plt.xlabel("Distancia (m)")
        plt.ylabel("Momento (kg-m)")
        plt.grid(True, linestyle='--')
        plt.axhline(0, color='black', linewidth=1)
        plt.legend()
        
        print(f"\nResultados: R={R:.2f}kg, Mmax={M_max:.2f}kg-m")
        plt.show()

    except ValueError:
        print("Error: Por favor, usa el punto (.) para decimales, no la coma.")

if __name__ == "__main__":
    calcular_viga_visual()