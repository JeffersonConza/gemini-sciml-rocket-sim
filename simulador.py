import argparse
import csv
import math
from motor_integracion import integrar_rk4

# --- Constantes Ambientales (Modelo de la Tierra) ---
G = 9.81         # Aceleración gravitacional (m/s^2)
V_EQ = 465.1     # Velocidad tangencial en el ecuador (m/s)
RHO_0 = 1.225    # Densidad del aire al nivel del mar (kg/m^3)
H_ESCALA = 8500  # Altura de escala atmosférica (m)

def cinematica_universal(t, estado, config):
    """
    Sistema unificado de Ecuaciones Diferenciales Ordinarias (EDOs).
    Calcula las derivadas para [x, y, vx, vy, m] basado en la configuración.
    """
    x, y, vx, vy, m = estado
    y_alt = max(0, y) # Evitar altitudes negativas por error numérico
    v_mag = math.sqrt(vx**2 + vy**2)
    
    # --- 1. Lógica de Etapas y Empuje (Thrust) ---
    # Implementamos una separación de etapa para mejorar la relación Empuje/Peso
    T_SEPARACION = 150.0 
    
    if m <= config.masa_vacio:
        T = 0
        dm_dt = 0
    elif t < T_SEPARACION:
        # Etapa 1: Gran empuje para vencer la gravedad inicial
        T = config.empuje
        dm_dt = -config.tasa_masa
    else:
        # Etapa 2: Motor optimizado para vacío (menor masa, mayor eficiencia)
        # Reducimos empuje pero bajamos drásticamente el consumo
        T = config.empuje * 0.6 
        dm_dt = -config.tasa_masa * 0.3 
        
    # --- 2. Resistencia Atmosférica (Drag) ---
    if config.drag and y_alt < 100000: # El drag es despreciable sobre los 100km
        rho = RHO_0 * math.exp(-y_alt / H_ESCALA)
        f_drag = 0.5 * rho * (v_mag**2) * config.cd * config.area if v_mag > 0.1 else 0
        ax_drag = -(f_drag / m) * (vx / v_mag) if v_mag > 0 else 0
        ay_drag = -(f_drag / m) * (vy / v_mag) if v_mag > 0 else 0
    else:
        ax_drag, ay_drag = 0, 0

    # --- 3. Perfil de Inclinación (Gravity Turn) ---
    if config.gravity_turn:
        if t < config.inicio_giro:
            theta = math.pi / 2 # Ascenso vertical puro
        else:
            # Maniobra de cabeceo gradual hacia la horizontal (0 rad)
            tasa_giro = (math.pi / 2) / config.duracion_giro
            theta = max(0.0, (math.pi / 2) - tasa_giro * (t - config.inicio_giro))
    else:
        theta = math.pi / 2 # Sin maniobra, ascenso 90 grados
        
    # --- 4. Ecuaciones de Movimiento ---
    dx_dt = vx
    dy_dt = vy
    
    # Descomposición de aceleración: (Empuje + Arrastre) / Masa - Gravedad
    dvx_dt = (T * math.cos(theta) / m) + ax_drag
    dvy_dt = (T * math.sin(theta) / m) - G + ay_drag
    
    return [dx_dt, dy_dt, dvx_dt, dvy_dt, dm_dt]

def main():
    parser = argparse.ArgumentParser(description="gemini-sciml-rocket-sim: Simulador Aeroespacial Multietapa")
    
    # Configuración del Vehículo
    parser.add_argument('--masa_inicial', type=float, default=300000, help='Masa inicial (kg)')
    parser.add_argument('--masa_vacio', type=float, default=50000, help='Masa final/estructural (kg)')
    parser.add_argument('--empuje', type=float, default=3500000, help='Empuje motor Etapa 1 (N)')
    parser.add_argument('--tasa_masa', type=float, default=1000, help='Consumo Etapa 1 (kg/s)')
    
    # Flags de Física
    parser.add_argument('--drag', action='store_true', help='Habilitar resistencia atmosférica')
    parser.add_argument('--cd', type=float, default=0.5, help='Coeficiente de arrastre')
    parser.add_argument('--area', type=float, default=10.0, help='Área frontal (m^2)')
    
    # Flags de Maniobra
    parser.add_argument('--gravity_turn', action='store_true', help='Habilitar maniobra de cabeceo')
    parser.add_argument('--inicio_giro', type=float, default=20.0, help='Inicio del pitch (s)')
    parser.add_argument('--duracion_giro', type=float, default=240.0, help='Tiempo para llegar a horizontal (s)')
    
    # Configuración Numérica
    parser.add_argument('--tiempo', type=float, default=400.0, help='Tiempo total (s)')
    parser.add_argument('--dt', type=float, default=0.1, help='Paso de integración (s)')
    parser.add_argument('--salida', type=str, default='telemetria.csv', help='Archivo de salida')
    
    args = parser.parse_args()
    
    # Estado inicial: [x, y, vx, vy, m]
    # Importante: vx inicia con V_EQ por la rotación terrestre en el ecuador
    estado_0 = [0.0, 0.0, V_EQ, 0.0, args.masa_inicial]
    
    print(f"--- Ejecutando simulación: {args.salida} ---")
    print(f"Config -> Drag: {args.drag} | Gravity Turn: {args.gravity_turn}")
    
    # Ejecutar integración RK4
    resultados = integrar_rk4(cinematica_universal, estado_0, (0.0, args.tiempo), args.dt, args)
    
    # Guardar resultados
    with open(args.salida, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['t', 'x', 'y', 'vx', 'vy', 'm'])
        writer.writerows(resultados)
        
    print(f"Simulación finalizada. Datos guardados en {args.salida}")

if __name__ == '__main__':
    main()