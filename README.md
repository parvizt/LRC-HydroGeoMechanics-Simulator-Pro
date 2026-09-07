⚡ LRC-HydroGeoMechanics Simulator Pro

Author: Parviz Tajdari (GitHub | LinkedIn) — Computational Geosciences & Numerical Geomechanics Framework

BadgeValue🐍 LanguagePython 3.9+🖥️ GUIPyQt5 | PyQtGraph🔬 ResearchLTU Ref: 4286-2026⚙️ PhysicsKirsch | Mohr-Coulomb | Poroelasticity🚀 Build2026.09.06 · v1.0.0



💡 This README is designed as a single self-contained canvas for the GitHub repository front page.

📌 Executive Summary & Research Scope



💡 Large-scale seasonal hydrogen storage is a key enabler of the fossil-free energy transition in hard-rock terrains such as northern Sweden.

Large-scale Underground Hydrogen Storage (UHS) in Lined Rock Caverns (LRCs) — excavated chambers in crystalline hard rock sealed with an engineered lining system — is a foundational pillar for northern Sweden's green transition (e.g., the HYBRIT initiative and fossil-free steelmaking). Recent coupled thermo–gas–mechanical studies confirm that cyclic charging–storage–discharging produces strongly stage-dependent temperature and pressure evolution, repeated stress redistribution around the cavern, and thermal cycling of the sealing layer and surrounding rock (Liang et al., 2026).

In this software, cyclical injection and withdrawal of compressed hydrogen gas ($H_2$) at pressures up to $25\ \text{MPa}$ subject the host crystalline rock and engineered liners to severe coupled Thermo-Hydro-Mechanical (THM) cyclic loads. The simulator captures this physics through an analytical coupling of Kirsch stress solutions, the Mohr-Coulomb failure criterion, and Biot poroelasticity, all exposed through a real-time PyQt5 desktop interface.

🛠️ Installation

Step 1 — Clone the repository:

git clone https://github.com/parvizt/LRC-HydroGeoMechanics-Simulator-Pro.git
cd LRC-HydroGeoMechanics-Simulator-Pro


Step 2 — Install dependencies:

pip install PyQt5 pyqtgraph numpy scipy


📦 Package🔧 PurposePyQt5Desktop GUI frameworkpyqtgraphScientific real-time plottingnumpyNumerical array operationsscipyODE solving & signal processing

Python 3.9+ is recommended. All dependencies are available via pip on Windows, Linux, and macOS.

▶️ Run

python lrc_simulator.py




🔑 Default login password: admin
🗄️ The SQLite database (lrc_geomechanics_sim.db) is created automatically on first launch — no manual setup required.

On the first run the AuthDialog opens; after authentication, the main LRCSimulatorPro window loads and all saved scenarios are read from the local SQLite store.

📁 Project Structure

📦 LRC-HydroGeoMechanics-Simulator-Pro/
│
├── 🐍  lrc_simulator.py          ← Main application entry point
├── 🗄️  lrc_geomechanics_sim.db   ← SQLite database (auto-created on first run)
├── 🖼️  l.ico                     ← Window icon (optional)
└── 📷  qr.png                    ← QR code image (optional)




🧮 Physics Modules

🔬 Module🧩 Role⚙️ CoupledTHMEngineCore analytical THM solver — Kirsch stress solution + Mohr-Coulomb criterion + Biot poroelasticity💾 DBManagerSQLite CRUD — save, load, and reset simulation scenarios🖥️ LRCSimulatorProMain PyQt5 window & UI controller🔐 AuthDialogLogin dialog with password-based authentication

The analytical pipeline of CoupledTHMEngine computes the circumferential and radial stress fields around the circular cavern from the Kirsch solution, evaluates yield with the Mohr-Coulomb criterion, and applies Biot's poroelastic coupling to capture the pore-pressure contribution of cyclic hydrogen injection.

📊 Input Parameters

🗂️ Category📐 Parameters🪨 GeologicalDepth H, cavern radius R, rock density ρ, lateral stress ratio K₀🔩 MechanicalUCS, friction angle φ, liner thickness t, Young's modulus E, Poisson's ratio ν💨 OperationalMin. pressure P_min, Max. pressure P_max, thermal delta ΔT, annual injection cycles N

Every scenario defined by these inputs is persisted through DBManager and can be reloaded later, enabling systematic sensitivity defined by these inputs is persisted through DBManager and can be reloaded later, enabling systematic sensitivity and fatigue comparisons across parameter sets.

🖼️ Screenshots
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-5.x-41CD52?style=flat-square&logo=qt&logoColor=white)
![pyqtgraph](https://img.shields.io/badge/pyqtgraph-visualization-orange?style=flat-square)
![NumPy](https://img.shields.io/badge/NumPy-scientific-013243?style=flat-square&logo=numpy)
![SciPy](https://img.shields.io/badge/SciPy-analytical-8CAAE6?style=flat-square&logo=scipy)
![SQLite](https://img.shields.io/badge/SQLite-persistence-003B57?style=flat-square&logo=sqlite)
![License](https://img.shields.io/badge/License-Research--Use-blueviolet?style=flat-square)


📸 Screenshots of the running application will be added here.

Main Simulation TabStress Profile ChartFatigue Analysis(coming soon)(coming soon)(coming soon)

👨‍💻 Developer & Footer

👤Parviz Tajdari — github.com/parvizt🔖Freelance — kwork.com/user/parvizt🌐Website — AiBrothersTools.ir



🔬 Developed for research purposes at Luleå University of Technology (LTU)
📌 LTU Internal Reference Code: 4286-2026

Built with ❤️ for geomechanical research — LRC Underground Hydrogen Storage Analysis




📚 Reference

Liang, Y., Chai, Y., Wang, X., Espley, S., & Yin, S. (2026). Hydrogen Underground Storage in Lined Rock Caverns in Southern Ontario, Canada. Mining, 6(3), 60.



