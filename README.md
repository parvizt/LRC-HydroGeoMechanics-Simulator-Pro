# 🔬 LRC-HydroGeoMechanics Simulator Pro

> **Luleå University Edition** | LTU Underground H₂ Storage Framework  
> 🏛️ Developed for LTU Ref: **4286-2026** | 🌐 [AiBrothersTools.ir](https://AiBrothersTools.ir)

---

## 🧾 Project Info

| Field | Details |
|-------|---------|
| 📦 **Version** | 1.0.0 (Build 2026.09.06) |
| 👤 **Author** | Parviz Tajdari — [github.com/parvizt](https://github.com/parvizt) |
| 🐍 **Python** | 3.9+ |
| 🖥️ **GUI** | PyQt5 |
| 📊 **Plotting** | pyqtgraph |
| 🗄️ **Database** | SQLite3 |
| 🔢 **Numerics** | NumPy · SciPy |

---

## 🚀 Features

- ⚙️ **Coupled THM Solver** — Thermo-Hydro-Mechanical analytical engine using modified Kirsch equations
- 📈 **Spatial Stress Profiling** — Radial & tangential stress distribution around lined rock caverns
- 🔄 **Cyclic Fatigue Analysis** — Steel liner Von Mises stress vs. S355 yield limit over injection/withdrawal cycles
- 🧱 **Plastic Zone Estimation** — Mohr-Coulomb failure criterion (Kastner-type analytical form)
- 💾r injection/withdrawal cycles
- 🧱 **Plastic Zone Estimation** — Mohr-Coulomb failure criterion (Kastner-type analytical form)
- 💾t: `admin`)
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


lrc_simulator.py       # Main application entry point
lrc_geomechanics_sim.db  # Auto-generated SQLite database (on first run)
d:/l.ico               # Optional window icon
d:/qr.png              # Optional QR image

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
|----------|-------- |
| `AuthDialog` | Password authentication dialog |

---

## 📊 Input Parameters

| Category | Parameters |
|----------|-----------|
| 🪨 **Geological** | Depth, Cavern Radius, Rock Density, K₀ |
|  Angle, Liner Thickness |
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


---
