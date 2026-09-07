## 🛠️ Installation

**Step 1 — Clone the repository:**
```bash
git clone https://github.com/parvizt/LRC-HydroGeoMechanics-Simulator-Pro.git
cd LRC-HydroGeoMechanics-Simulator-Pro

**Step 2 — Install dependencies:**
bash
pip install PyQt5 pyqtgraph numpy scipy

<div align="center">

| 📦 Package | 🔧 Purpose |
|:----------:|:-----------|
| `PyQt5` | Desktop GUI framework |
| `pyqtgraph` | Scientific real-time plotting |
| `numpy` | Numerical array operations |
| `scipy` | ODE solving & signal processing |

</div>

---

## ▶️ Run

bash
python lrc_simulator.py

> 🔑 **Default login password:** `admin`  
> 🗄️ SQLite database is created automatically on first launch.

---

## 📁 Project Structure


📦 LRC-HydroGeoMechanics-Simulator-Pro/
│
├── 🐍  lrc_simulator.py          ← Main application entry point
├── 🗄️  lrc_geomechanics_sim.db   ← SQLite database (auto-created on first run)
├── 🖼️  d:/l.ico                  ← Window icon (optional)
└── 📷  d:/qr.png                 ← QR code image (optional)

---

## 🧮 Physics Modules

<div align="center">

| 🔬 Module | 🧩 Role |
|:---------:|:--------|
| ⚙️ `CoupledTHMEngine` | Core analytical THM solver — Kirsch + Mohr-Coulomb + Biot poroelasticity |
| 💾 `DBManager` | SQLite CRUD — save, load, and reset simulation scenarios |
| 🖥️ `LRCSimulatorPro` | Main PyQt5 window & UI controller |
| 🔐 `AuthDialog` | Login dialog with password-based authentication |

</div>

---

## 📊 Input Parameters

<div align="center">

| 🗂️ Category | 📐 Parameters |
|:-----------:|:-------------|
| 🪨 **Geological** | Depth `H`, cavern radius `R`, rock density `ρ`, lateral stress ratio `K₀` |
| 🔩 **Mechanical** | UCS, friction angle `φ`, liner thickness `t`, Young's modulus `E`, Poisson's ratio `ν` |
| 💨 **Operational** | Min. pressure `P_min`, Max. pressure `P_max`, thermal delta `ΔT`, annual injection cycles `N` |

</div>

---

## 🖼️ Screenshots

> 📸 *Add your application screenshots here.*

| Main Simulation Tab | Stress Profile Chart | Fatigue Analysis |
|:-------------------:|:--------------------:|:----------------:|
| *(coming soon)* | *(coming soon)* | *(coming soon)* |

---

## 👨‍💻 Developer

<div align="center">

| | |
|:-:|:--|
| 👤 | **Parviz Tajdari** — [github.com/parvizt](https://github.com/parvizt) |
| 🔖 | Freelance — [kwork.com/user/parvizt](https://kwork.com/user/parvizt) |
| 🌐 | Website — [AiBrothersTools.ir](https://AiBrothersTools.ir) |

</div>

<br>

> 🔬 Developed for research purposes at **Luleå University of Technology (LTU)**  
> 📌 LTU Internal Reference Code: `4286-2026`

---

<div align="center">

*Built with ❤️ for geomechanical research — LRC Underground Hydrogen Storage Analysis*

[![GitHub](https://img.shields.io/badge/GitHub-parvizt-181717?style=flat-square&logo=github)](https://github.com/parvizt)
[![Website](https://img.shields.io/badge/Web-AiBrothersTools.ir-0A66C2?style=flat-square&logo=internetexplorer)](https://AiBrothersTools.ir)

</div>


---
