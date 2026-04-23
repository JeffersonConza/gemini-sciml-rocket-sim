# 🚀 SciML Aerospace Simulator: De la EDO al Reporte Automatizado

Este proyecto es un ecosistema de simulación numérica diseñado para modelar la dinámica de vuelo de cohetes desde el ecuador terrestre. Integra la resolución de **Ecuaciones Diferenciales Ordinarias (EDOs)** mediante un motor Runge-Kutta de 4to orden (RK4) con un pipeline de análisis automatizado mediante **Gemini CLI**.

## 📊 Propósito del Proyecto
El objetivo es generar datos sintéticos de alta fidelidad (*Ground Truth*) para comparar tres escenarios de vuelo:
1.  **Modelo Ideal:** Lanzamiento sin resistencia atmosférica (vuelo balístico puro).
2.  **Modelo Realista:** Incorporación de resistencia atmosférica (Drag) no lineal.
3.  **Modelo de Inserción Orbital:** Implementación de una maniobra de cabeceo (*Gravity Turn*) para maximizar la velocidad tangencial.



## 🛠️ Arquitectura Técnica

El sistema está construido bajo principios de **modularidad** y **automatización**:

* **`motor_integracion.py`**: Implementación vectorial del método **Runge-Kutta (RK4)** en Python puro. Diseñado para ser agnóstico al problema, permitiendo integrar sistemas de cualquier dimensión.
* **`simulador.py`**: Motor físico unificado que modela el empuje, la masa variable (quema de combustible), el drag atmosférico exponencial y la trigonometría del *Gravity Turn*.
* **`generar_reporte.sh`**: Orquestador en Bash que gestiona el ciclo de vida de los datos: Ejecución → Validación → Auditoría por IA.

### Formulación Matemática
El simulador resuelve el siguiente sistema de EDOs acopladas:

$$\frac{d\vec{v}}{dt} = \frac{\vec{T}(\theta, t)}{m(t)} + \vec{g} - \frac{\vec{F}_d(\rho, v)}{m(t)}$$

Donde la densidad atmosférica $\rho$ decae exponencialmente con la altitud $y$:
$$\rho(y) = \rho_0 e^{-y/H}$$

## 🚀 Instalación y Uso

### Requisitos
* Python 3.x
* Node.js & Gemini CLI (`npm install -g @google/gemini-cli`)
* Entorno Linux/ChromeOS (Crostini)

### Ejecución del Pipeline Completo
Para ejecutar todas las simulaciones y generar el reporte técnico analizado por IA, simplemente corre:

```bash
chmod +x generar_reporte.sh
./generar_reporte.sh
