# 🚀 gemini-sciml-rocket-sim  
### Physics-Informed Machine Learning | Scientific Computing | Aerospace Simulation

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SciML](https://img.shields.io/badge/SciML-FF6F00?style=for-the-badge)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-0A66C2?style=for-the-badge)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Gemini CLI](https://img.shields.io/badge/Gemini%20CLI-4285F4?style=for-the-badge&logo=google-gemini&logoColor=white)

---

## 📌 Overview

**gemini-sciml-rocket-sim** is a **Scientific Machine Learning (SciML)** project that combines:

- 🚀 Aerospace simulation  
- 🧮 Numerical methods (RK4)  
- 🤖 AI-assisted analysis (LLMs)  

to generate **high-quality synthetic physics data** for training **Physics-Informed Neural Networks (PINNs)**.

> 💡 Designed as a **portfolio-grade project** demonstrating real-world skills in:
> Machine Learning Engineering, Data Science, Scientific Computing, and Applied Mathematics

---

## 🎯 Key Features

- ✅ Custom **Runge-Kutta 4 (RK4)** solver (no external dependencies)  
- ✅ End-to-end **data pipeline (simulation → CSV → AI analysis)**  
- ✅ Realistic **rocket dynamics (drag, thrust, gravity, mass depletion)**  
- ✅ **PINNs-ready datasets**  
- ✅ Integration with **Gemini CLI for automated engineering analysis**  
- ✅ Clean modular architecture (Python + Bash orchestration)  

---

## 🎥 Demo

![Rocket Simulation Demo](./rocket_simulation.gif)

---

## 🧠 Skills Demonstrated

### Machine Learning Engineering
- Synthetic data generation  
- Physics-informed datasets  
- Pipeline design  

### Scientific Computing
- Numerical ODE solving (RK4)  
- Stability and precision  
- Continuous dynamical systems  

### Applied Mathematics
- Nonlinear differential equations  
- Fluid dynamics (drag modeling)  
- Trajectory optimization  

### Software Engineering
- Modular architecture  
- CLI pipelines  
- Reproducibility  

### AI + LLM Integration
- Automated telemetry auditing  
- Engineering reasoning with LLMs  

---

## ⚙️ Mathematical Model

The simulator models **2D rocket flight dynamics** using nonlinear ODEs.

### State Vector

$$
\mathbf{u}(t) = [x, y, v_x, v_y, m]^T
$$

### Governing Equations

**Kinematics**
$$
\dot{x} = v_x, \quad \dot{y} = v_y
$$

**Dynamics**
$$
\dot{v}_x = \frac{T \cos(\theta)}{m} - \frac{F_d}{m}\frac{v_x}{v}
$$

$$
\dot{v}_y = \frac{T \sin(\theta)}{m} - g - \frac{F_d}{m}\frac{v_y}{v}
$$

**Mass Depletion**
$$
\dot{m} = -\dot{m}_{rate}
$$

---

## 🗂️ Project Structure

```text
gemini-sciml-rocket-sim/
│
├── motor_integracion.py   # RK4 numerical solver
├── simulador.py           # Rocket dynamics simulator
├── generar_reporte.sh     # Pipeline automation
├── data/                  # Generated telemetry (CSV)
└── reports/               # AI-generated analysis
```

---

## 🔄 Data Pipeline

`Simulation Engine` → `CSV Telemetry` → `Gemini CLI` → `Engineering Report`

### Components

1. RK4 Solver → Accurate trajectory integration  
2. Simulator → Scenario generation  
3. Bash Script → Automation  
4. LLM Audit → Insight extraction  

---

## 🚀 Simulation Scenarios

- 🟢 Ideal (no drag)  
- 🔵 Drag-limited  
- 🔴 Gravity Turn (orbital trajectory)  

---

## 📊 Why This Project Matters

- Demonstrates **real ML data generation**, not just modeling  
- Bridges **physics + machine learning (SciML)**  
- Shows ability to:
  - Build numerical solvers from scratch  
  - Design end-to-end pipelines  
  - Apply theory to real systems  

---

## 🧬 Applications

- Physics-Informed Neural Networks (PINNs)  
- Aerospace trajectory optimization  
- Scientific simulations  
- Synthetic data generation for ML  

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.x  
- Node.js (v20+)  
- Gemini CLI (authenticated)  

---

### ▶️ Run the Project

```bash
chmod +x generar_reporte.sh
./generar_reporte.sh
```

---

## 📈 Outputs

- 📄 CSV telemetry (position, velocity, mass vs time)
- 📊 AI-generated reports:
  - Delta-v analysis
  - Energy loss
  - Trajectory efficiency

---

## 👤 Author

**Jefferson A. Conza**  
Mathematics Student | Aspiring Machine Learning Engineer  

🔬 Interests:
- Scientific Machine Learning  
- Deep Learning  
- Computational Physics  
