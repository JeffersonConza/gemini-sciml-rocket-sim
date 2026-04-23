I will now draft a professional `README.md` for the `gemini-sciml-rocket-sim` repository, incorporating the mathematical framework, data pipeline architecture, and comparative efficiency analysis as requested.

```markdown
# gemini-sciml-rocket-sim

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-Script-green?logo=gnu-bash&logoColor=white)
![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-AI_Auditor-orange?logo=google-gemini&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A High-Fidelity Synthetic Data Generator for Scientific Machine Learning (SciML) and PINNs.**

## Abstract

This repository provides a robust framework for generating multi-stage aerospace telemetry using numerical integration of Ordinary Differential Equations (ODEs). Designed as a "Ground Truth" engine for Physics-Informed Neural Networks (PINNs), the system simulates rocket dynamics including atmospheric drag, gravity turns, and mass depletion. A unique feature of this pipeline is the integration of **Gemini CLI**, which acts as an AI Mission Auditor, performing heuristic analysis on the generated telemetry to validate orbital efficiency and mission viability.

## Mathematical Framework

The core of the simulator resides in the `cinematica_universal` function, which solves a system of non-linear ODEs using a 4th-order Runge-Kutta (RK4) method. The state vector is defined as $\mathbf{s} = [x, y, v_x, v_y, m]^T$.

### Governing Equations

The dynamics are governed by the following system:

$$
\begin{cases} 
\dot{x} = v_x \\
\dot{y} = v_y \\
\dot{v}_x = \frac{T(t) \cos(\theta)}{m} + a_{x, drag} \\
\dot{v}_y = \frac{T(t) \sin(\theta)}{m} - g + a_{y, drag} \\
\dot{m} = \dot{m}_{thrust}
\end{cases}
$$

Where:
*   **Thrust ($T$):** Piecewise function representing a two-stage propulsion system.
*   **Atmospheric Drag ($a_{drag}$):** Modeled using the exponential barometric formula:
    $$\rho(y) = \rho_0 e^{-y/H_{scale}}$$
    $$F_{drag} = \frac{1}{2} \rho(y) v^2 C_d A$$
*   **Gravity Turn ($\theta$):** A time-dependent pitch maneuver $\theta(t)$ that transitions from vertical ascent ($\pi/2$) to horizontal orbital injection ($0$).

## Data Pipeline Architecture

The project employs a three-layer architecture designed for Scientific ML workflows:

1.  **Ground Truth Generation (`simulador.py` & `motor_integracion.py`):** A library-independent RK4 engine calculates high-precision trajectories. It produces raw telemetry in CSV format, serving as the training target for PINNs.
2.  **Orchestration (`generar_reporte.sh`):** A shell pipeline that automates multiple physical scenarios: Ideal (Vacuum), Atmospheric (Drag), and Orbital (Gravity Turn).
3.  **AI Auditing (Gemini CLI):** The `gemini` agent ingests the multi-scenario CSV data. It performs cross-validation, calculating Delta-v gains and energy loss coefficients, effectively acting as a "Mission Control" analyst that interprets numerical data into structural insights.

## Comparative Analysis: Gravity Turn vs. Vertical Ascent

Based on the implemented physics, the simulator demonstrates the following efficiencies:

*   **Gravity Turn:** By initiating a pitch maneuver (default at $t=20s$), the vehicle utilizes gravity to rotate its velocity vector. This minimizes "Gravity Losses" by converting vertical potential energy into the horizontal kinetic energy ($v_x$) required for stable orbits. The code initializes $v_x$ with Earth's tangential velocity ($V_{EQ} \approx 465.1$ m/s) to simulate equatorial launch assists.
*   **Vertical Ascent:** In simulations without the `--gravity_turn` flag, the vehicle maintains $\theta = \pi/2$. While this reaches higher peak altitudes, the $v_x$ remains static, resulting in a zero-eccentricity "fall-back" trajectory, proving inefficient for orbital deployment as it fails to achieve the necessary tangential velocity.

## Getting Started

### Prerequisites
- Python 3.x
- Gemini CLI (configured with API access)

### Execution
Run the unified pipeline to generate synthetic data and the AI-powered technical report:
```bash
chmod +x generar_reporte.sh
./generar_reporte.sh
```

The results will be available in `reporte_vuelo.md`, providing a deep-dive into the flight dynamics and stage-separation efficiency.

---
**Jefferson Conza**  
*Mathematics Student & ML Engineer*
