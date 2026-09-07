# ⚡ LRC-HydroGeoMechanics Simulator Pro

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-5.x-41CD52?style=flat-square&logo=qt&logoColor=white)
![pyqtgraph](https://img.shields.io/badge/pyqtgraph-visualization-orange?style=flat-square)
![NumPy](https://img.shields.io/badge/NumPy-scientific-013243?style=flat-square&logo=numpy)
![SciPy](https://img.shields.io/badge/SciPy-analytical-8CAAE6?style=flat-square&logo=scipy)
![SQLite](https://img.shields.io/badge/SQLite-persistence-003B57?style=flat-square&logo=sqlite)
![License](https://img.shields.io/badge/License-Research--Use-blueviolet?style=flat-square)

**Author:** [Parviz Tajdari](https://github.com/parvizt) ([LinkedIn](https://www.linkedin.com/in/parviz-tajdari-69364925a)) — *Computational Geosciences & Numerical Geomechanics Framework*

| Badge | Value |
| :--- | :--- |
| 🐍 Language | Python 3.9+ |
| 🖥️ GUI | PyQt5 | PyQtGraph |
| 🔬 Research | LTU Ref: 4286-2026 |
| ⚙️ Physics | Kirsch | Mohr-Coulomb | Poroelasticity |
| 🚀 Build | 2026.09.06 · v1.0.0 |


<img width="1536" height="1024" alt="lrc" src="https://github.com/user-attachments/assets/24541adc-f2eb-414a-a643-6fcd865ff2d0" />

---

## 📌 2. Executive Summary & Research Scope

💡 **Large-scale seasonal hydrogen storage is a key enabler of the fossil-free energy transition in hard-rock terrains such as northern Sweden.**

Large-scale **Underground Hydrogen Storage (UHS)** in **Lined Rock Caverns (LRCs)** — excavated chambers in crystalline hard rock sealed with an engineered lining system — is a foundational pillar for northern Sweden’s green transition (e.g., the HYBRIT initiative and fossil-free steelmaking). Recent coupled thermo–gas–mechanical studies confirm that cyclic charging–storage–discharging produces strongly stage-dependent temperature and pressure evolution, repeated stress redistribution around the cavern, and thermal cycling of the sealing layer and surrounding rock (Liang et al., 2026).

In this software, cyclical injection and withdrawal of compressed hydrogen gas ($H_2$) at pressures up to **25 MPa** subject the host crystalline rock and engineered liners to severe coupled **Thermo-Hydro-Mechanical (THM)** cyclic loads. The simulator captures this physics through an analytical coupling of Kirsch stress solutions, the Mohr-Coulomb failure criterion, and Biot poroelasticity, all exposed through a real-time PyQt5 desktop interface.

---

## 🛠️ 3. Installation

**Step 1 — Clone the repository:**
```bash
git clone https://github.com/parvizt/LRC-HydroGeoMechanics-Simulator-Pro.git
cd LRC-HydroGeoMechanics-Simulator-Pro
```

**Step 2 — Install dependencies:**
```bash
pip install PyQt5 pyqtgraph numpy scipy
```

| 📦 Package | 🔧 Purpose |
| :--- | :--- |
| **PyQt5** | Desktop GUI framework |
| **pyqtgraph** | Scientific real-time plotting |
| **numpy** | Numerical array operations |
| **scipy** | ODE solving & signal processing |

---

## ▶️ 4. Run

```bash
python lrc_simulator.py
```

🔑 **Default login password:** `admin`  
🗄️ *The SQLite database (`lrc_geomechanics_sim.db`) is created automatically on first launch — no manual setup required.*

On the first run, the `AuthDialog` opens; after authentication, the main `LRCSimulatorPro` window loads and all saved scenarios are read from the local SQLite store.

---

## 📁 5. Project Structure

```text
📦 LRC-HydroGeoMechanics-Simulator-Pro/
│
├── 🐍  lrc_simulator.py          ← Main application entry point
├── 🗄️  lrc_geomechanics_sim.db   ← SQLite database (auto-created)
├── 🖼️  l.ico                     ← Window icon (optional)
└── 📷  qr.png                    ← QR code image (optional)
```

---

## 🧮 6. Physics Modules

| 🔬 Module | 🧩 Role |
| :--- | :--- |
| **⚙️ CoupledTHMEngine** | Core analytical THM solver — Kirsch stress solution + Mohr-Coulomb criterion + Biot poroelasticity |
| **💾 DBManager** | SQLite CRUD — save, load, and reset simulation scenarios |
| **🖥️ LRCSimulatorPro** | Main PyQt5 window & UI controller |
| **🔐 AuthDialog** | Login dialog with password-based authentication |

---

## 📊 7. Input Parameters

| 🗂️ Category | 📐 Parameters |
| :--- | :--- |
| 🪨 **Geological** | Depth $H$, cavern radius $R$, rock density $\rho$, lateral stress ratio $K_0$ |
| 🔩 **Mechanical** | UCS, friction angle $\phi$, liner thickness $t$, Young's modulus $E$, Poisson's ratio $\nu$ |
| 💨 **Operational** | Min. pressure $P_{min}$, Max. pressure $P_{max}$, thermal delta $\Delta T$, annual cycles $N$ |

---

## 🖼️ 8. Screenshots

| Main Simulation Tab | Stress Profile Chart | Fatigue Analysis |
| <img width="1919" height="987" alt="1" src="https://github.com/user-attachments/assets/5d55c014-96b3-47a1-8e44-becff8f314a2" /> 
|<img width="1920" height="986" alt="2" src="https://github.com/user-attachments/assets/2a615cf2-49f4-4d6d-bc9f-9a68477dbef8" /> 
| <img width="1920" height="989" alt="3" src="https://github.com/user-attachments/assets/54efcccd-2fc5-467b-94ad-708f526eb861" /> |


---

## 👨‍💻 9. Developer & Footer

👤 **Parviz Tajdari** — [github.com/parvizt](https://github.com/parvizt)  
🔖 **Freelance** — [kwork.com/user/parvizt](https://kwork.com/user/parvizt)  
🌐 **Website** — [AiBrothersTools.ir](https://AiBrothersTools.ir)

🔬 *Developed for research purposes at Luleå University of Technology (LTU)*  
📌 *LTU Internal Reference Code: 4286-2026*

*Built with ❤️ for geomechanical research — LRC Underground Hydrogen Storage Analysis*

---

### 📚 9.1 Reference
Liang, Y., Chai, Y., Wang, X., Espley, S., & Yin, S. (2026). Hydrogen Underground Storage in Lined Rock Caverns in Southern Ontario, Canada. *Mining*, 6(3), 60.
