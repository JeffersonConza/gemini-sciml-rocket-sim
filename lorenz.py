import csv

def lorenz_system(t, state, sigma=10.0, rho=28.0, beta=8/3):
    """
    Define las ecuaciones diferenciales del sistema de Lorenz.
    state: lista [x, y, z]
    """
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

def rk4_step(f, t, state, dt):
    """
    Calcula un paso de integración utilizando Runge-Kutta de 4to orden.
    f: función que devuelve las derivadas (f(t, state))
    t: tiempo actual
    state: lista con los valores actuales de las variables
    dt: tamaño del paso temporal
    """
    # k1 = f(t, state)
    k1 = f(t, state)
    
    # k2 = f(t + dt/2, state + dt/2 * k1)
    state_k2 = [state[i] + (dt / 2.0) * k1[i] for i in range(len(state))]
    k2 = f(t + dt / 2.0, state_k2)
    
    # k3 = f(t + dt/2, state + dt/2 * k2)
    state_k3 = [state[i] + (dt / 2.0) * k2[i] for i in range(len(state))]
    k3 = f(t + dt / 2.0, state_k3)
    
    # k4 = f(t + dt, state + dt * k3)
    state_k4 = [state[i] + dt * k3[i] for i in range(len(state))]
    k4 = f(t + dt, state_k4)
    
    # state_next = state + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)
    new_state = [
        state[i] + (dt / 6.0) * (k1[i] + 2.0*k2[i] + 2.0*k3[i] + k4[i])
        for i in range(len(state))
    ]
    
    return new_state

def simulate(f, initial_state, t_start, t_end, dt):
    """
    Ejecuta la simulación completa y devuelve la historia de estados.
    """
    results = []
    t = t_start
    state = initial_state
    
    # Guardar estado inicial
    results.append([t] + state)
    
    while t < t_end:
        state = rk4_step(f, t, state, dt)
        t += dt
        results.append([t] + state)
        
    return results

def save_to_csv(filename, data):
    """
    Guarda los datos en un archivo CSV.
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['t', 'x', 'y', 'z'])
        writer.writerows(data)

if __name__ == "__main__":
    # Parámetros de la simulación
    initial_state = [1.0, 1.0, 1.0]  # [x0, y0, z0]
    t_start = 0.0
    t_end = 50.0
    dt = 0.01
    
    # Ejecutar simulación
    print(f"Simulando sistema de Lorenz desde t={t_start} hasta t={t_end}...")
    data = simulate(lorenz_system, initial_state, t_start, t_end, dt)
    
    # Exportar a CSV
    output_file = 'datos_lorenz.csv'
    save_to_csv(output_file, data)
    print(f"Resultados exportados a '{output_file}'.")
