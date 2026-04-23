import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import os

def generar_animacion(input_csv='datos_orbitales.csv', output_file='trayectoria.gif'):
    """
    Lee datos de telemetría y genera una animación de la trayectoria del cohete.
    """
    
    # 1. Lectura de datos usando la librería estándar csv
    if not os.path.exists(input_csv):
        print(f"Error: El archivo '{input_csv}' no existe.")
        print(f"Sugerencia: Ejecuta el simulador para generar datos (ej: python3 simulador.py --salida {input_csv})")
        return

    t_data, x_data, y_data = [], [], []
    
    try:
        with open(input_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                t_data.append(float(row['t']))
                x_data.append(float(row['x']))
                y_data.append(float(row['y']))
    except KeyError as e:
        print(f"Error: Formato de CSV incorrecto. Falta la columna: {e}")
        return
    except Exception as e:
        print(f"Error leyendo el archivo: {e}")
        return

    if not t_data:
        print("El archivo está vacío.")
        return

    # 2. Configuración de la figura de Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Límites del gráfico basados en los datos (con margen)
    ax.set_xlim(min(x_data) - 5000, max(x_data) + 5000)
    ax.set_ylim(0, max(y_data) * 1.1)
    
    ax.set_xlabel("Distancia Horizontal (m)")
    ax.set_ylabel("Altitud (m)")
    ax.set_title("Trayectoria del Cohete")
    ax.grid(True, linestyle='--', alpha=0.6)

    # Elementos de la animación
    linea_trayectoria, = ax.plot([], [], 'b-', lw=1.5, label='Trayectoria') # Estela
    cohete, = ax.plot([], [], 'ro', markersize=6, label='Cohete')           # Marcador
    texto_tiempo = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    ax.legend(loc='upper right')

    # 3. Funciones para FuncAnimation
    def init():
        linea_trayectoria.set_data([], [])
        cohete.set_data([], [])
        texto_tiempo.set_text('')
        return linea_trayectoria, cohete, texto_tiempo

    # Reducimos frames para que la animación no sea excesivamente pesada (downsampling)
    step = max(1, len(t_data) // 200) # Apuntamos a ~200 frames para el GIF
    indices = range(0, len(t_data), step)

    def update(frame_idx):
        # Actualizar estela (todos los puntos hasta el actual)
        linea_trayectoria.set_data(x_data[:frame_idx], y_data[:frame_idx])
        
        # Actualizar posición actual del cohete
        cohete.set_data([x_data[frame_idx]], [y_data[frame_idx]])
        
        # Actualizar etiqueta de tiempo
        texto_tiempo.set_text(f'Tiempo: {t_data[frame_idx]:.1f}s | Altitud: {y_data[frame_idx]/1000:.2f}km')
        
        return linea_trayectoria, cohete, texto_tiempo

    # 4. Crear la animación
    print("Generando animación (esto puede tardar unos segundos)...")
    ani = animation.FuncAnimation(
        fig, update, frames=indices, init_func=init, 
        blit=True, interval=50, repeat=False
    )

    # 5. Guardar el archivo
    try:
        # Intentamos guardar como GIF (requiere Pillow instalado: pip install pillow)
        print(f"Guardando animación en '{output_file}'...")
        ani.save(output_file, writer='pillow', fps=20)
        print("¡Éxito! Animación guardada.")
    except Exception as e:
        print(f"Error al guardar la animación: {e}")
        print("Asegúrate de tener instalada la librería 'pillow' (pip install pillow) para generar GIFs.")

    plt.close()

if __name__ == "__main__":
    # Nombre del archivo por defecto o pasado por argumento
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'datos_orbitales.csv'
    generar_animacion(input_file)
