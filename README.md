# ⚡ LRC-HydroGeoMechanics Simulator Pro

**Author:** [Parviz Tajdari](https://github.com/parvizt) ([LinkedIn](https://www.linkedin.com/in/parviz-tajdari-69364925a)) — *Computational Geosciences & Numerical Geomechanics Framework*

| Badge | Value |
| :--- | :--- |
| 🐍 Language | Python 3.9+ |
| 🖥️ GUI | PyQt5 · PyQtGraph |
| 🔬 Research | LTU Ref: 4286-2026 |
| ⚙️ Physics | Kirsch · Mohr-Coulomb · Poroelasticity |
| 🚀 Build | 2026.09.06 · v1.0.0 |

---

## 📌 Executive Summary & Research Scope

💡 **Large-scale seasonal hydrogen storage is a key enabler of the fossil-free energy transition in hard-rock terrains such as northern Sweden.**

Large-scale **Underground Hydrogen Storage (UHS)** in **Lined Rock Caverns (LRCs)** — excavated chambers in crystalline hard rock sealed with an engineered lining system — is a foundational pillar for northern Sweden's green transition (e.g., the HYBRIT initiative and fossil-free steelmaking). Recent coupled thermo–gas–mechanical studies confirm that cyclic charging–storage–discharging produces strongly stage-dependent temperature and pressure evolution, repeated stress redistribution around the cavern, and thermal cycling of the sealing layer and surrounding rock (Liang et al., 2026).

In this software, cyclical injection and withdrawal of compressed hydrogen gas (H₂) at pressures up to **25 MPa** subject the host crystalline rock and engineered liners to severe coupled **Thermo-Hydro-Mechanical (THM)** cyclic loads. The simulator captures this physics through an analytical coupling of Kirsch stress solutions, the Mohr-Coulomb failure criterion, and Biot poroelasticity, all exposed through a real-time PyQt5 desktop interface.

---

## 🛠️ Installation

**Step 1 — Clone the repository:**
```bash
git clone https://github.com/parvizt/LRC-HydroGeoMechanics-Simulator-Pro.git
cd LRC-HydroGeoMechanics-Simulator-Pro

**Step 2 — Install dependencies:**

bash
pip install PyQt5 pyqtgraph numpy scipy

| 📦 Package | 🔧 Purpose |
| :--- | :--- |
| PyQt5 | Desktop GUI framework |
| pyqtgraph | Scientific real-time plotting |
| numpy | Numerical array operations |
| scipy | ODE solving & signal processing |

---

## ▶️ Run

bash| scipy | ODE solving & signal processing |

---

## ▶️ Run

```bash🗄️ The SQLite database (`lrc_geomechanics_sim.db`) is created automatically on first launch — no manual setup required.

On the first run, the `AuthDialog` opens; after authentication, the main `LRCSimulatorPro` window loads and all saved scenarios are read from the local SQLite store.

---

## 📁 Project Structure
```text
📦 LRC-HydroGeoMechanics-Simulator-Pro/
│
├── 🐍  lrc_simulator.py          ← Main application entry point
├── 🗄️  lrc_geomechanics_sim.db   ← SQLite database (auto-created)
├── 🖼️  l.ico                     ← Window icon (optional)
└── 📷  qr.png                    ← QR code image (optional)

---

## 🧮 Physics Modules

| 🔬 Module | 🧩 Role |
| :--- | :--- |
| ⚙️ CoupledTHMEngine | Core analytical THM solver — Kirsch stress solution + Mohr-Coulomb criterion + Biot poroelasticity |
| 💾 DBManager | SQLite CRUD — save, load, and reset simulation scenarios |
| 🖥️ LRCSimulatorPro | Main PyQt5 window & UI controller |
| 🔐 AuthDialog | Login dialog with password-based authentication |

---

## 📊 Input Parameters

| 🗂️ Category | 📐 Parameters |
| :--- | :--- |
| 🪨 Geological | Depth `H`, cavern radius `R`, rock density `ρ`, lateral stress ratio `K₀` |
| 🔩 Mechanical | UCS, friction angle `φ`, liner thickness `t`, Young's modulus `E`, Poisson's ratio `ν` |
| 💨 Operational | Min. pressure `P_min`, Max. pressure `P_max`, thermal delta `ΔT`, annual cycles `N` |

---

## 🖼️ Screenshots

| Main Simulation Tab | Stress Profile Chart | Fatigue Analysis |
<img width="1920" height="987" alt="image" src="https://github.com/user-attachments/assets/613a53a7-2fbc-4242-b07e-c48843422dfb" />
<img width="1920" height="986" alt="image" src="https://github.com/user-attachments/assets/c761cc98-246d-4599-abfc-6a42073de252" />
<img width="1920" height="988" alt="image" src="https://github.com/user-attachments/assets/ae34c749-b222-4630-ab81-61dbed315188" />




---

## 👨‍💻 Developer & Footer

- 👤 **Parviz Tajdari** — [github.com/parvizt](https://github.com/parvizt)
- 🔖 **Freelance** — [kwork.com/user/parvizt](https://kwork.com/user/parvizt)
- 🌐 **Website** — [AiBrothersTools.ir](https://AiBrothersTools.ir)
- 🔬 Developed for research purposes at **Luleå University of Technology (LTU)**
- 📌 **LTU Internal Reference Code:** `4286-2026`

> Built with ❤️ for geomechanical research — **LRC Underground Hydrogen Storage Analysis**

---

## 📚 Reference

Liang, Y., Chai, Y., Wang, X., Espley, S., & Yin, S. (2026). *Hydrogen Underground Storage in Lined Rock Caverns in Southern Ontario, Canada.* Mining, 6(3), 60.


---
