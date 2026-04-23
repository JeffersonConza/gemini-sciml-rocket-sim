# gemini-sciml-rocket-sim 🚀
### Synthetic Data Generation for Physics-Informed Neural Networks (PINNs)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SciML](https://img.shields.io/badge/SciML-FF6F00?style=for-the-badge)
![Applied Mathematics](https://img.shields.io/badge/Mathematics-003153?style=for-the-badge)
![Aerospace](https://img.shields.io/badge/Aerospace-NASA-blue?style=for-the-badge)
![Gemini CLI](https://img.shields.io/badge/Gemini%20CLI-4285F4?style=for-the-badge&logo=google-gemini&logoColor=white)

---

## 📌 Project Vision

**gemini-sciml-rocket-sim** is a high-fidelity data generation engine designed for **Scientific Machine Learning (SciML)**. Its primary purpose is to produce "Ground Truth" datasets that satisfy explicit physical constraints, enabling the training and validation of **Physics-Informed Neural Networks (PINNs)**.

By bridging numerical integration (RK4) with AI-driven auditing (Gemini), this project demonstrates a modern pipeline where simulation data is not just generated, but autonomously analyzed for energy efficiency and mission viability.

---

## 🏗️ Architecture & Data Pipeline

The project implements a robust "Simulation-to-Insight" loop:

1.  **Numerical Engine (`motor_integracion.py`):** A custom 4th-order Runge-Kutta (RK4) solver ensures high precision in time-stepping for non-linear systems.
2.  **Physics Simulator (`simulador.py`):** Implements multi-stage rocket dynamics, including barometric drag models and gravity turn maneuvers.
3.  **Automation Layer (`generar_reporte.sh`):** Orchestrates multiple simulation scenarios (Ideal, Drag-limited, Orbital).
4.  **AI Auditor (Gemini CLI):** Acts as a Chief Mission Engineer, performing zero-shot reasoning over the generated CSV telemetry to compare Delta-v gains and energy losses.

---

## 🧠 Mathematical Framework

The simulation solves a system of five coupled first-order Ordinary Differential Equations (ODEs) describing the state vector $\mathbf{u}(t) = [x, y, v_x, v_y, m]^T$.

### Governing Equations

$$
\frac{d}{dt} \begin{bmatrix} x \\ y \\ v_x \\ v_y \\ m \end{bmatrix} = 
\begin{bmatrix} 
v_x \\ 
v_y \\ 
\frac{T(t) \cos(\theta)}{m} + a_{drag, x} \\ 
\frac{T(t) \sin(\theta)}{m} - g + a_{drag, y} \\ 
-\dot{m}(t) 
\end{bmatrix}
$$

### Variable Mass & Multi-Stage Logic
The thrust $T(t)$ and mass flow rate $\dot{m}(t)$ follow a piecewise definition to simulate stage separation at $t_{sep} = 150s$:

$$
(T, \dot{m}) = \begin{cases} (T_1, \dot{m}_1) & t < t_{sep} \\ (0.6 T_1, 0.3 \dot{m}_1) & t \ge t_{sep} \end{cases}
$$

### Atmospheric Drag Model
Drag is calculated using a dynamic air density $\rho(y)$ based on a scale-height $H_{scale} \approx 8500m$:

$$
\rho(y) = \rho_0 e^{-\frac{y}{H_{scale}}}
$$
$$
\mathbf{a}_{drag} = -\frac{1}{2m} \rho(y) \|\mathbf{v}\|^2 C_d A \frac{\mathbf{v}}{\|\mathbf{v}\|}
$$

### Trajectory Profiles: Gravity Turn
The pitch angle $\theta$ evolves to minimize gravity losses by gaining horizontal velocity:

$$
\theta(t) = \begin{cases} \pi/2 & t < t_{start} \\ \max(0, \frac{\pi}{2} - \omega (t - t_{start})) & t \ge t_{start} \end{cases}
$$

---

## 🚀 Mission Scenarios: Vertical vs. Gravity Turn

The platform allows for deep physical comparisons:

*   **Vertical Ascent:** A naive climb where $v_x$ remains constant ($V_{earth\_rotation}$). It suffers from maximum gravity losses as the thrust vector remains parallel to gravity for the entire flight.
*   **Gravity Turn:** A highly efficient maneuver that uses Earth's gravity to rotate the velocity vector toward the horizontal plane. This expands the horizontal Delta-v, which is critical for achieving stable orbital velocity.

---

## 🧬 Why Use This for PINNs?

Traditional Neural Networks require massive amounts of data. **PINNs**, however, use physical laws (like the ODEs above) as a regularization term in the loss function:

$$
\mathcal{L} = \mathcal{L}_{data} + \mathcal{L}_{physics}
$$

This repository provides the high-resolution synthetic telemetry needed for the $\mathcal{L}_{data}$ term, while the explicit mathematical model defined in `simulador.py` provides the exact derivatives for the $\mathcal{L}_{physics}$ constraint.

---

## 🛠️ Usage

To execute the complete SciML pipeline and generate the AI engineering report:

```bash
chmod +x generar_reporte.sh
./generar_reporte.sh
```

### Generated Outputs:
*   `datos_lanzamiento.csv`: Ideal vacuum flight.
*   `datos_lanzamiento_drag.csv`: Atmospheric flight with energy losses.
*   `datos_orbitales.csv`: Optimized gravity turn trajectory.
*   `reporte_vuelo.md`: AI-powered physical validation and analysis.

---

**Jefferson Conza**  
*Mathematics Student & ML Engineer*
