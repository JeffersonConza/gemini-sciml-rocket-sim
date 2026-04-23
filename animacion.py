import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.collections import LineCollection
import numpy as np
import sys
import os

# --- Parámetros de Diseño y Sincronización ---
DURACION_OBJETIVO = 15.0  # Duración total exacta en segundos
NUM_FRAMES_DESEADOS = 300 # Resolución temporal de la animación
LINEA_KARMAN = 100000
VEL_SONIDO = 340.0

# Colores Accesibles
C_CIAN_SUAVE = '#4DD0E1'
C_NARANJA_SUAVE = '#FFB74D'
C_AMARILLO_SUAVE = '#FFF176'
C_MAGENTA_PASTEL = '#F06292'
C_CIAN_APAGADO = '#4DB6AC'

# Parámetros Físicos (Sincronizados con simulador.py)
G = 9.81
RHO_0 = 1.225
H_ESCALA = 8500
EMPUJE_S1 = 3500000
CD = 0.5
AREA = 10.0
T_SEPARACION = 150.0
INICIO_GIRO = 20.0
DURACION_GIRO = 240.0

def cargar_datos(input_csv):
    if not os.path.exists(input_csv):
        return None
    data = {'t': [], 'x': [], 'y': [], 'vx': [], 'vy': [], 'm': []}
    try:
        with open(input_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                for key in data:
                    data[key].append(float(row[key]))
        return {k: np.array(v) for k, v in data.items()}
    except Exception as e:
        print(f"Error cargando CSV: {e}")
        return None

def generar_trayectoria_basica(data, output_file='trayectoria.gif'):
    """Genera una animación limpia y accesible de la trayectoria."""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    
    t, x, y = data['t'], data['x'], data['y']
    step = max(1, len(t) // NUM_FRAMES_DESEADOS)
    idx_frames = range(0, len(t), step)
    total_f = len(idx_frames)
    
    # Sincronización
    intervalo_ms = (DURACION_OBJETIVO * 1000) / total_f
    fps_save = total_f / DURACION_OBJETIVO

    ax.set_title("TRAYECTORIA DE VUELO - VISTA BÁSICA", color='white', pad=15)
    ax.set_xlabel("Distancia (m)", color=C_CIAN_SUAVE)
    ax.set_ylabel("Altitud (m)", color=C_CIAN_SUAVE)
    ax.grid(True, linestyle='--', alpha=0.2)
    
    linea, = ax.plot([], [], color=C_CIAN_SUAVE, lw=2, label='Trayectoria')
    cohete, = ax.plot([], [], marker='o', color=C_NARANJA_SUAVE, markersize=8)
    hud = ax.text(0.02, 0.95, '', transform=ax.transAxes, family='monospace', fontsize=10)

    # Limites estáticos con margen
    ax.set_xlim(min(x) - 5000, max(x) + 5000)
    ax.set_ylim(0, max(y) * 1.1)

    def update(i):
        linea.set_data(x[:i], y[:i])
        cohete.set_data([x[i]], [y[i]])
        hud.set_text(f"TIEMPO: {t[i]:.1f} s\nALTITUD: {y[i]/1000:.2f} km")
        return linea, cohete, hud

    print(f"Renderizando {output_file} ({total_f} frames)...")
    ani = animation.FuncAnimation(fig, update, frames=idx_frames, interval=intervalo_ms, blit=True)
    ani.save(output_file, writer='pillow', fps=fps_save)
    plt.close()

def generar_validacion_avanzada(data, output_file='validacion_fisica_sciml.gif'):
    """Genera la herramienta avanzada SciML con DCL y estela termodinámica."""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 7), dpi=100)
    
    t, x, y, vx, vy, m = data['t'], data['x'], data['y'], data['vx'], data['vy'], data['m']
    v_mags = np.sqrt(vx**2 + vy**2)
    
    step = max(1, len(t) // NUM_FRAMES_DESEADOS)
    idx_frames = range(0, len(t), step)
    total_f = len(idx_frames)
    
    # Sincronización
    intervalo_ms = (DURACION_OBJETIVO * 1000) / total_f
    fps_save = total_f / DURACION_OBJETIVO

    ax.set_title("SISTEMA DE VALIDACIÓN FÍSICA SciML", color='white', fontweight='bold', pad=20)
    ax.axhspan(0, LINEA_KARMAN, color='#1A237E', alpha=0.1) # Atmósfera sutil
    ax.axhline(LINEA_KARMAN, color=C_MAGENTA_PASTEL, linestyle=':', alpha=0.4)
    
    # Estela con colormap magma (colorblind friendly)
    lc = LineCollection([], cmap='magma', lw=2, alpha=0.9)
    ax.add_collection(lc)
    
    # Sprite Triangular de Actitud
    rocket_base = np.array([[1200, 0], [-600, -400], [-600, 400]])
    rocket_patch = patches.Polygon(rocket_base, closed=True, color='white', ec=C_CIAN_SUAVE, lw=1)
    ax.add_patch(rocket_patch)

    # DCL Quiver
    dcl = ax.quiver([0,0,0], [0,0,0], [0,0,0], [0,0,0], 
                    color=[C_AMARILLO_SUAVE, C_MAGENTA_PASTEL, C_CIAN_APAGADO], 
                    scale=1, units='xy', width=200, headwidth=4)

    hud_box = dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.7, edgecolor=C_CIAN_SUAVE)
    hud = ax.text(0.02, 0.97, '', transform=ax.transAxes, family='monospace', fontsize=9, va='top', bbox=hud_box)
    alerta = ax.text(0.5, 0.6, '', transform=ax.transAxes, ha='center', fontsize=12, color=C_AMARILLO_SUAVE, fontweight='bold')

    def update(i):
        # Cálculos físicos para el frame
        curr_t, curr_y, curr_m = t[i], max(0, y[i]), m[i]
        v_vec = np.array([vx[i], vy[i]])
        v_mag = v_mags[i]
        
        # Actitud
        theta = np.pi/2 if curr_t < INICIO_GIRO else max(0.0, (np.pi/2) - ((np.pi/2)/DURACION_GIRO)*(curr_t - INICIO_GIRO))
        
        # Fuerzas
        thrust_m = 0 if curr_m <= 50000 else (EMPUJE_S1 if curr_t < T_SEPARACION else EMPUJE_S1 * 0.6)
        f_t = np.array([thrust_m * np.cos(theta), thrust_m * np.sin(theta)])
        
        rho = RHO_0 * np.exp(-curr_y / H_ESCALA) if curr_y < LINEA_KARMAN else 0
        f_d_m = 0.5 * rho * (v_mag**2) * CD * AREA if v_mag > 0.1 else 0
        f_d = -(f_d_m * (v_vec / v_mag)) if v_mag > 0.1 else np.zeros(2)
        f_g = np.array([0, -curr_m * G])
        
        acc = np.linalg.norm((f_t + f_d + f_g) / curr_m)
        twr = thrust_m / (curr_m * G) if curr_m > 0 else 0
        mach = v_mag / VEL_SONIDO

        # Visuales
        rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        rocket_patch.set_xy(rocket_base @ rot.T + [x[i], y[i]])
        
        if i > 1:
            pts = np.array([x[:i+1], y[:i+1]]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            lc.set_segments(segs)
            lc.set_array(v_mags[:i])

        esc = 0.012 * (1 + y[i]/30000)
        dcl.set_offsets(np.c_[[x[i]]*3, [y[i]]*3])
        dcl.set_UVC([f_t[0]*esc, f_d[0]*esc, f_g[0]*esc], [f_t[1]*esc, f_d[1]*esc, f_g[1]*esc])

        # Auto-zoom
        margen = 8000 + y[i]*0.15
        ax.set_xlim(min(x) - 4000, max(x[i] + margen, 40000))
        ax.set_ylim(0, max(y[i] + margen, LINEA_KARMAN * 1.1))

        if 150 <= curr_t < 165:
            alerta.set_text("SEPARACIÓN DE ETAPA CONFIRMADA")
            rocket_patch.set_color(C_AMARILLO_SUAVE)
        else:
            alerta.set_text("")
            rocket_patch.set_color('white')

        hud.set_text(
            f"TIEMPO: {curr_t:06.1f} s | MACH: {mach:4.2f}\n"
            f"----------------------------------\n"
            f"ALTITUD     : {y[i]/1000:8.2f} km\n"
            f"DISTANCIA   : {x[i]/1000:8.2f} km\n"
            f"VELOCIDAD   : {v_mag/1000:8.2f} km/s\n"
            f"ACELERACIÓN : {acc:8.2f} m/s²\n"
            f"REL. EMPUJE : {twr:8.2f} (TWR)\n"
            f"MASA ACTUAL : {curr_m/1000:8.2f} tons"
        )
        return lc, rocket_patch, dcl, hud, alerta

    print(f"Renderizando {output_file} ({total_f} frames)...")
    ani = animation.FuncAnimation(fig, update, frames=idx_frames, interval=intervalo_ms, blit=False)
    ani.save(output_file, writer='pillow', fps=fps_save)
    plt.close()

if __name__ == "__main__":
    archivo_csv = sys.argv[1] if len(sys.argv) > 1 else 'datos_orbitales.csv'
    datos = cargar_datos(archivo_csv)
    
    if datos:
        print("--- Iniciando Proceso de Visualización Dual ---")
        generar_trayectoria_basica(datos)
        generar_validacion_avanzada(datos)
        print("--- Visualizaciones completadas con éxito ---")
    else:
        print(f"Error fatal: No se pudieron cargar datos de {archivo_csv}")
