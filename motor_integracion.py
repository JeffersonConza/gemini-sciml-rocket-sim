# motor_integracion.py

def rk4_step(f, t, y, dt, *args):
    """
    Calcula un único paso de integración usando Runge-Kutta de 4to orden.
    Soporta vectores (listas) de dimensión N sin usar librerías externas.
    """
    # k1
    k1 = f(t, y, *args)
    
    # k2
    y_k2 = [yi + 0.5 * dt * k1i for yi, k1i in zip(y, k1)]
    k2 = f(t + 0.5 * dt, y_k2, *args)
    
    # k3
    y_k3 = [yi + 0.5 * dt * k2i for yi, k2i in zip(y, k2)]
    k3 = f(t + 0.5 * dt, y_k3, *args)
    
    # k4
    y_k4 = [yi + dt * k3i for yi, k3i in zip(y, k3)]
    k4 = f(t + dt, y_k4, *args)
    
    # Combinar para el siguiente paso
    y_next = [yi + (dt / 6.0) * (k1i + 2*k2i + 2*k3i + k4i) 
              for yi, k1i, k2i, k3i, k4i in zip(y, k1, k2, k3, k4)]
    
    return y_next

def integrar_rk4(f, y0, t_span, dt, *args):
    """
    Integra un sistema de EDOs desde t0 hasta tf.
    Retorna una lista de tuplas con la evolución temporal: [(t, y1, y2...), ...]
    """
    t0, tf = t_span
    t = t0
    y = y0
    
    resultados = [(t, *y)]
    
    while t < tf:
        # Ajustar el último paso para no pasarnos de tf
        if t + dt > tf:
            dt = tf - t
            
        y = rk4_step(f, t, y, dt, *args)
        t += dt
        resultados.append((t, *y))
        
    return resultados
