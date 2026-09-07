<div align="center">

# ⚡ LRC-HydroGeoMechanics Simulator Pro ⚡

### 🧪 Coupled Thermo-Hydro-Mechanical (THM) Framework  
### for Underground Hydrogen Storage (UHS) in Lined Rock Caverns

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5%20%7C%20PyQtGraph-green.svg?style=for-the-badge&logo=qt&logoColor=white)](https://riverbankcomputing.com/software/pyqt/)
[![Research](https://img.shields.io/badge/Research-LTU%20Ref%3A%204286--2026-orange.svg?style=for-the-badge&logo=sciencedirect&logoColor=white)](https://www.ltu.se)
[![Geomechanics](https://img.shields.io/badge/Physics-Kirsch%20%7C%20Mohr--Coulomb%20%7C%20Poroelasticity-red.svg?style=for-the-badge)]()
[![Build](https://img.shields.io/badge/Build-2026.09.06%20v1.0.0-purple.svg?style=for-the-badge)]()

</div>

---

## 🧾 Project Info

| Field | Details |
|-------|---------|
| 📦 **Version** | `1.0.0` — Build `2026.09.06` |
| 👤 **Author** | Parviz Tajdari — [github.com/parvizt](https://github.com/parvizt) |
| 🐍 **Python** | 3.9+ |
| 🖥️ **GUI** | PyQt5 |
| 📊 **Plotting** | pyqtgraph |
| 🗄️ **Database** | SQLite3 |
| 🔬 **Solver** | Coupled THM Analytical Engine |
| 🏛️ **Institution** | Luleå University of Technology (LTU) |
| 🌐 **Website** | [AiBrothersTools.ir](https://AiBrothersTools.ir) |

---

## 🚀 Features

- ⚙️ **Coupled THM Solver** — Thermo-Hydro-Mechanical analytical engine using modified Kirsch equations
- 📈 **Spatial Stress Profiling** — Radial & tangential stress distribution around lined rock caverns
- 🔄 **Cyclic Fatigue Analysis** — Steel liner Von Mises stress vs. S355 yield limit over injection/withdrawal cycles
- 🧱 **Plastic Zone Estimation** — Mohr-Coulomb failure criterion (Kastner-type analytical form)
- 💾 **Scenario Database** — Save, load, and reset simulation scenarios via SQLite
- 🔐 **Auth Protection** — Password-protected access (default: `admin`)
- 🎨 **Multi-Theme UI** — Classic · Dark · Pro · Orange · Pink
- 🔍 **Zoom Control** — Dynamic font & UI scaling

---
<div align="center">

## 🛠️ Installation
```bash
pip install PyQt5 pyqtgraph numpy scipy

| Package | Purpose |
|---------|---------|
| `PyQt5` | Desktop GUI framework |
| `pyqtgraph` | Scientific real-time plotting |
| `numpy` | Numerical array operations |
| `scipy` | ODE solving & signal processing |
</div>

---

## ▶️ Run

bash
python lrc_simulator.py

> 🔑 **Default password:** `admin`

---

## 📁 Project Structure


📦 LRC-HydroGeoMechanics-Simulator-Pro/
├── 🐍 lrc_simulator.py            ← Main application entry point
├── 🗄️ lrc_geomechanics_sim.db     ← SQLite database (auto-created on first run)
├── 🖼️ d:/l.ico                    ← Window icon (optional)
└── 📷 d:/qr.png                   ← QR code image (optional)

---

## 🧮 Physics Modules

| Module | Role |
|--------|------|
| ⚙️ `CoupledTHMEngine` | Core analytical THM solver (Kirsch + Mohr-Coulomb + Biot) |
| 💾 `DBManager` | SQLite CRUD — save, load, reset scenarios |
| 🖥️ `LRCSimulatorPro` | Main PyQt5 window & UI controller |
| 🔐 `AuthDialog` | Login dialog with password authentication |

---

## 📊 Input Parameters

| Category | Parameters |
|----------|-----------|
| 🪨 **Geological** | Depth, cavern radius, rock density, lateral stress ratio *K₀* |
| 🔩 **Mechanical** | UCS, friction angle, liner thickness, Young's modulus *E*, Poisson's ratio *ν* |
| 💨 **Operational** | *P_min*, *P_max*, thermal delta *ΔT*, annual injection cycles |

---

## 🖼️ Screenshots

> 📸 *Add your application screenshots here*

---

## 👨‍💻 Developer

| | |
|-|-|
| 👤 **Author** | [Parviz Tajdari](https://github.com/parvizt) |
| 🔖 **Watermark** | [kwork/user/parvizt](https://kwork.com/user/parvizt) |
| 🌐 **Website** | [AiBrothersTools.ir](https://AiBrothersTools.ir) |

> 🔬 Developed for research purposes at **Luleå University of Technology (LTU)**  
> 📌 LTU Reference: `4286-2026`

---

<div align="center">

*Built with ❤️ for geomechanical research — LRC Hydrogen Storage Analysis*

</div>
