I will now generate a professional `README.md` for the `gemini-sciml-rocket-sim` repository, incorporating the mathematical framework, pipeline architecture, and SciML context as requested.

I will use the `generalist` agent to create the `README.md` file with the professional documentation, mathematical framework, and SciML context, as it has access to the necessary file-writing tools.

I will provide the professional `README.md` content formatted as a research paper, including the mathematical framework in LaTeX and the detailed pipeline architecture, as the current environment restricts direct file writing.

# gemini-sciml-rocket-sim

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Gemini CLI](https://img.shields.io/badge/Gemini%20CLI-4285F4?style=for-the-badge&logo=google-gemini&logoColor=white)

## Abstract
`gemini-sciml-rocket-sim` is a high-fidelity aerospace simulation framework designed for **Scientific Machine Learning (SciML)** applications. It serves as a robust synthetic data generator for training **Physics-Informed Neural Networks (PINNs)**, providing ground-truth telemetry via a custom Runge-Kutta 4th Order (RK4) integration engine. The project integrates traditional numerical methods with LLM-based telemetry auditing, creating a closed-loop pipeline for mission analysis and physical validation.

---

## 1. Mathematical Framework

The simulator solves a system of non-linear Ordinary Differential Equations (ODEs) representing the 2D planar motion of a launch vehicle.

### 1.1 State Vector
The system state at time $t$ is defined as:
$$\mathbf{u}(t) = \begin{bmatrix} x & y & v_x & v_y & m \end{bmatrix}^T$$

### 1.2 Governing Equations
The dynamics are governed by the following coupled ODEs:

1.  **Kinematics:**
    $$\dot{x} = v_x, \quad \dot{y} = v_y$$
2.  **Dynamics (Newton's Second Law):**
    $$\dot{v}_x = \frac{T \cos(\theta) + F_{D,x}}{m}$$
    $$\dot{v}_y = \frac{T \sin(\theta) + F_{D,y}}{m} - g$$
3.  **Mass Depletion:**
    $$\dot{m} = -\dot{m}_{thrust}$$

### 1.3 Physical Models
*   **Atmospheric Drag ($F_D$):** Modeled using the drag equation $F_D = \frac{1}{2} \rho v^2 C_d A$, where density $\rho$ follows the barometric formula $\rho(y) = \rho_0 e^{-y/H}$.
*   **Thrust ($T$):** Implements a two-stage logic where Stage 1 provides high initial thrust to overcome gravity, and Stage 2 optimizes for vacuum efficiency.
*   **Initial Conditions:** The simulation accounts for Earth's rotational velocity at the equator ($V_{EQ} \approx 465.1$ m/s) as an initial horizontal boost.

---

## 2. Data Pipeline Architecture

The system operates as a unified **Ground Truth Generator & AI Auditor** pipeline:

1.  **Numerical Engine (`motor_integracion.py`):** A library-independent RK4 integrator ensures high precision for SciML training sets, where minimizing numerical drift is critical for PINN loss functions.
2.  **Dynamic Simulator (`simulador.py`):** Generates high-resolution CSV telemetry across multiple scenarios (Ideal, Drag-limited, and Gravity Turn).
3.  **Orchestration (`generar_reporte.sh`):** Automates the execution of the experimental matrix.
4.  **AI Audit (Gemini CLI):** Acts as the **Chief Mission Engineer**. It consumes the raw CSV telemetry to perform energy loss analysis, Delta-v calculations, and structural feasibility assessments.

---

## 3. Mission Analysis: Gravity Turn vs. Vertical Ascent

The simulator provides empirical evidence of orbital efficiency:

| Parameter | Vertical Ascent | Gravity Turn |
| :--- | :--- | :--- |
| **Gravity Loss** | Maximum ($\int g \cdot dt$) | Minimized via vectoring |
| **Horizontal Velocity** | Static (Relies on $V_{EQ}$) | Exponentially increased |
| **Energy Profile** | Potential Energy heavy | Kinetic Energy optimized |

By initiating a **Pitchover Maneuver** ($\theta$ transition from $\pi/2$ to $0$), the vehicle converts thrust into horizontal velocity, utilizing the Earth's curvature to reach orbital velocity while minimizing atmospheric residence time.

---

## 4. Synthetic Data for PINNs

This repository is optimized for researchers building Physics-Informed Neural Networks. The output datasets allow for:
*   **Residual Minimization:** Training networks where the loss function includes the ODE residuals from Section 1.
*   **Parameter Identification:** Using noisy telemetry to regress unknown coefficients like $C_d$ or $I_{sp}$.
*   **Extrapolation Testing:** Validating ML models on multi-stage transitions and atmospheric density gradients.

---

## 5. Getting Started

### Prerequisites
*   Python 3.x
*   [Gemini CLI](https://github.com/google/gemini-cli)

### Execution
Run the complete unified pipeline:
```bash
chmod +x generar_reporte.sh
./generar_reporte.sh
```
This will generate `reporte_vuelo.md`, containing the AI-driven analysis of the simulated flight dynamics.
