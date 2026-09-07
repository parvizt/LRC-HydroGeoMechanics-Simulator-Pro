<div align="center">

# ⚡ LRC-HydroGeoMechanics Simulator Pro ⚡

### 🧪 Coupled Thermo-Hydro-Mechanical (THM) Framework for Underground Hydrogen Storage (UHS) in Lined Rock Caverns

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5%20%7C%20PyQtGraph-green.svg?style=for-the-badge&logo=qt&logoColor=white)](https://riverbankcomputing.com/software/pyqt/)
[![Research](https://img.shields.io/badge/Research-LTU%20Ref%3A%204286--2026-orange.svg?style=for-the-badge&logo=sciencedirect&logoColor=white)](https://www.ltu.se)
[![Geomechanics](https://img.shields.io/badge/Physics-Kirsch%20%7C%20Mohr--Coulomb%20%7C%20Poroelasticity-red.svg?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Build-2026.09.06%20v1.0.0-purple.svg?style=for-the-badge)]()

</div>

---

## 🧾 Project Info

| Field | Details |
|-------|---------|
| 📦 **Version** | 1.0.0 (Build 2026.09.06) |
| 👤 **Author** | Parviz Tajdari — [github.com/parvizt](https://github.com/parvizt) |
| 🐍 **Python** | 3.9+ |
| 🖥️ **GUI** | PyQt5 |
| 📊 **Plotting** | pyqtgraph |
| 🗄️ **Database** | SQL THM Solver** — Thermo-Hydro-Mechanical analytimPy · SciPy |

---

## 🚀 Features

- ⚙️ **Coupled THM Solver** — Thermo-Hydro-Mechanical analytical engine using modified Kirsch equations
- 📈 **Spatial Stress Profiling** — Radial & tangential stress distribution around lined rock caverns
- 🔄 **Cyclic Fatigue Analysis** — Steel liner Von Mises stress vs. S355 yield limit over injection/withdrawal cycles
- 🧱 **Plastic Zone Estimation** — Mohr-Coulomb failure criterion (Kastner-type analytical form)
- 💾 **Scenario Database** — Save, load, and reset simulation scenarios via SQLite
- 🔐 **Auth Protection** — Password-protected access (default: `admin`)
- 🎨 **Multi-Theme UI** — Pro · Dark · Classic · Pink
- 🔍 **Zoom Control** — Dynamic font & UI scaling

---

## 🛠️ Requirements
```bash
pip install PyQt5 pyqtgraph numpy scipy

---

## ▶️ Run

bash
python lrc_simulator.py

> 🔑 Default password: `admin`

---

## 📁 Project Structure


lrc_simulator.py          # Main application entry point
lrc_geomechanics_sim.db   # Auto-generated SQLite database (on first run)
d:/l.ico                  # Optional window icon
d:/qr.png                 # Optional QR image

---

## 🧮 Physics Modules

| Module | Description |
|--------|-------------|
| `CoupledTHMEngine` | Core THM analytical solver |
| `DBManager` | SQLite CRUD for simulation records |
| `LRCSimulatorPro` | Main PyQt5 GUI application window |
| `AuthDialog` | Password authentication dialog |

---

## 📊 Input Parameters

| Category | Parameters |
|----------|-----------|
| 🪨 **Geological** | Depth, Cavern Radius, Rock Density, K₀ |
| 🔩 **Mechanical** | UCS, Friction Angle, Liner Thickness, E, ν |
| 💨 **Operational** | P_min, P_max, ΔT (thermal), Annual Injection Cycles |

---

## 🖼️ Screenshots

> *(Add screenshots here)*

---

## 📜 License

This project is developed for research purposes at **Luleå University of Technology (LTU)**.  
🔖 Watermark: [kwork/user/parvizt](https://kwork.com/user/parvizt)

---

<div align="center">
  Built with ❤️ by <a href="https://github.com/parvizt">Parviz Tajdari</a> · <a href="https://AiBrothersTools.ir">AiBrothersTools.ir</a>
</div>


تغییرات اعمال‌شده:
- Features: موارد تکراری حذف، `💾` و `🔐` درست اضافه شد
- Requirements: بلاک کد درست بسته شد
- Project Structure: بلاک `code` صحیح
- Input Parameters: تکرار حذف، ردیف Mechanical با پارامترهای واقعی اضافه شد
- Physics Modules: جدول با alignment درست
