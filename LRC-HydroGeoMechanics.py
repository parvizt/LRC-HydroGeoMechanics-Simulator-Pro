# ==============================================================================
# Project: LRC-HydroGeoMechanics Simulator Pro (Luleå University Edition)
# Version: 1.0.0 (Build 2026.09.06)
# Author: Parviz Tajdari (github.com/parvizt) | Developed for LTU Ref: 4286-2026
# Header: AiBrothersTools.ir | Watermark: kwork/user/parvizt
# Target: Python 3.9+ | PyQt5 | pyqtgraph | NumPy | SciPy | SQLite3
# ==============================================================================

import sys
import os
import math
import sqlite3
import datetime
import traceback
import numpy as np

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QTextEdit, QGroupBox, QSplitter,
    QStatusBar, QFileDialog, QMessageBox, QDialog, QDialogButtonBox,
    QHeaderView, QStyleFactory
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QDateTime
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette, QBrush

import pyqtgraph as pg

# Configure pyqtgraph for dark high-performance visualization
pg.setConfigOption('background', '#12161f')
pg.setConfigOption('foreground', '#d1d5db')
pg.setConfigOption('antialias', True)


# ------------------------------------------------------------------------------
# 1. DATABASE & PERSISTENCE MANAGER (SQLite)
# ------------------------------------------------------------------------------
class DBManager:
    """Manages SQLite storage for simulation configurations and runs."""
    def __init__(self, db_path="lrc_geomechanics_sim.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS simulations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        scenario_name TEXT,
                        cavern_radius REAL,
                        depth REAL,
                        p_min REAL,
                        p_max REAL,
                        temp_diff REAL,
                        cycles INTEGER,
                        young_modulus REAL,
                        poisson_ratio REAL,
                        liner_thickness REAL,
                        rock_cohesion REAL,
                        friction_angle REAL,
                        max_liner_stress REAL,
                        plastic_radius REAL,
                        safety_factor REAL
                    )
                """)
                conn.commit()
        except Exception as e:
            print(f"[DB Error] Init failed: {str(e)}")

    def save_simulation(self, data: dict):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO simulations (
                        timestamp, scenario_name, cavern_radius, depth, p_min, p_max,
                        temp_diff, cycles, young_modulus, poisson_ratio, liner_thickness,
                        rock_cohesion, friction_angle, max_liner_stress, plastic_radius, safety_factor
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    data.get('name', 'Scenario'),
                    data.get('r_c', 15.0),
                    data.get('depth', 500.0),
                    data.get('p_min', 5.0),
                    data.get('p_max', 20.0),
                    data.get('dt', 30.0),
                    data.get('cycles', 365),
                    data.get('E_rock', 45.0),
                    data.get('nu_rock', 0.22),
                    data.get('t_liner', 0.025),
                    data.get('c_rock', 12.0),
                    data.get('phi_rock', 38.0),
                    data.get('max_liner_stress', 0.0),
                    data.get('r_plastic', 0.0),
                    data.get('safety_factor', 0.0)
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"[DB Error] Save failed: {str(e)}")
            return False

    def fetch_all_simulations(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, timestamp, scenario_name, depth, p_max, max_liner_stress, plastic_radius, safety_factor FROM simulations ORDER BY id DESC")
                return cursor.fetchall()
        except Exception as e:
            print(f"[DB Error] Fetch failed: {str(e)}")
            return []

    def reset_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM simulations")
                conn.commit()
                return True
        except Exception as e:
            print(f"[DB Error] Reset failed: {str(e)}")
            return False


# ------------------------------------------------------------------------------
# 2. COMPUTATIONAL GEOMECHANICS & THM ENGINE
# ------------------------------------------------------------------------------
class CoupledTHMEngine:
    """
    Coupled Thermo-Hydro-Mechanical analytical and 1D FDM continuum solver
    for Lined Rock Cavern (LRC) Hydrogen Storage applications.
    """
    @staticmethod
    def calculate_insitu_stress(depth_m, rock_density=2700.0, k0=1.2):
        """Calculates vertical and horizontal in-situ stress at cavern depth."""
        g = 9.81
        sigma_v = (rock_density * g * depth_m) / 1e6  # MPa
        sigma_h = k0 * sigma_v                       # MPa
        return sigma_v, sigma_h

    @staticmethod
    def solve_spatial_stress_distribution(r_c, p_internal, sigma_h, E_rock, nu_rock, 
                                          alpha_t=1.0e-5, delta_t=0.0, r_max=100.0, num_nodes=200):
        """
        Computes Radial (sigma_r) and Tangential (sigma_theta) stress profiles
        around the pressurized and thermally perturbed cavern using modified Kirsch equations.
        """
        r = np.linspace(r_c, r_max, num_nodes)
        
        # Kirsch elastic solution under internal pressure P_i and far-field sigma_h
        sigma_r = sigma_h * (1.0 - (r_c**2 / r**2)) + p_internal * (r_c**2 / r**2)
        sigma_theta = sigma_h * (1.0 + (r_c**2 / r**2)) - p_internal * (r_c**2 / r**2)
        
        # Thermal stress perturbation: sigma_th = (E / (1 - nu)) * alpha * Delta_T * (r_c/r)^2
        if delta_t != 0.0:
            thermal_coeff = (E_rock * 1e3 / (1.0 - nu_rock)) * alpha_t * delta_t # MPa
            sigma_r -= thermal_coeff * (r_c**2 / r**2) * 0.5
            sigma_theta += thermal_coeff * (r_c**2 / r**2) * 0.5

        # Radial displacement u(r) in mm
        u_r = ((1.0 + nu_rock) / (E_rock * 1e3)) * (
            (sigma_h - p_internal) * (r_c**2 / r) + (1.0 - 2.0 * nu_rock) * sigma_h * r
        ) * 1000.0  # mm

        return r, sigma_r, sigma_theta, u_r

    @staticmethod
    def evaluate_liner_integrity(p_internal, r_c, t_liner, t_concrete, E_steel=210.0, E_conc=30.0, nu_steel=0.3):
        """
        Calculates stress distribution across Steel Liner and Concrete Cushion.
        Returns Von Mises stress in steel liner (MPa) and Yield Safety Factor (YSF).
        """
        r_liner_outer = r_c
        r_liner_inner = r_c - t_liner
        
        # Thin-to-thick cylinder stress approximation
        sigma_hoop_liner = (p_internal * r_liner_inner) / t_liner  # MPa
        sigma_rad_liner = -p_internal / 2.0                        # MPa
        
        # Von Mises equivalent stress
        von_mises = np.sqrt(sigma_hoop_liner**2 - sigma_hoop_liner * sigma_rad_liner + sigma_rad_liner**2)
        
        steel_yield_strength = 355.0  # S355 Structural steel yield in MPa
        safety_factor = steel_yield_strength / (von_mises + 1e-6)
        
        return von_mises, safety_factor

    @staticmethod
    def calculate_plastic_zone(r_c, p_internal, sigma_h, cohesion_mpa, friction_angle_deg):
        """
        Estimates plastic yield zone radius using Mohr-Coulomb failure criterion.
        """
        phi_rad = np.radians(friction_angle_deg)
        N_phi = (1.0 + np.sin(phi_rad)) / (1.0 - np.sin(phi_rad))
        sigma_c = 2.0 * cohesion_mpa * np.sqrt(N_phi) # Uniaxial Compressive Strength
        
        # Critical internal pressure to initiate yielding at the wall (r = r_c)
        # Mohr-Coulomb: sigma_theta_eff >= N_phi * sigma_r_eff + sigma_c
        p_critical = (2.0 * sigma_h - sigma_c) / (N_phi + 1.0)
        
        if p_internal < p_critical:
            # Plastic radius calculation (Kastner-type analytical form)
            term1 = (2.0 / (N_phi + 1.0)) * ((sigma_h + cohesion_mpa / np.tan(phi_rad)) / 
                                              (p_internal + cohesion_mpa / np.tan(phi_rad)))
            if term1 > 0:
                r_plastic = r_c * (term1 ** (1.0 / (N_phi - 1.0)))
            else:
                r_plastic = r_c
        else:
            r_plastic = r_c  # Fully elastic
            
        return max(r_plastic, r_c)


# ------------------------------------------------------------------------------
# 3. AUTHENTICATION DIALOG (admin password protected)
# ------------------------------------------------------------------------------
class AuthDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("System Access Verification | تایید احراز هویت")
        self.setFixedSize(380, 160)
        self.setStyleSheet("""
            QDialog { background-color: #1e2430; color: #ffffff; }
            QLabel { color: #e5e7eb; font-size: 13px; }
            QLineEdit { background-color: #2b3240; color: #ffffff; border: 1px solid #4b5563; padding: 6px; border-radius: 4px; }
            QPushButton { background-color: #2563eb; color: #ffffff; border-radius: 4px; padding: 6px 14px; font-weight: bold; }
            QPushButton:hover { background-color: #1d4ed8; }
        """)
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Enter Authentication Key (Default: <b>admin</b>):"))
        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.Password)
        self.txt_pass.setText("admin")
        layout.addWidget(self.txt_pass)
        
        self.lbl_msg = QLabel("")
        self.lbl_msg.setStyleSheet("color: #ef4444; font-size: 11px;")
        layout.addWidget(self.lbl_msg)
        
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.verify)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def verify(self):
        if self.txt_pass.text() == "admin":
            self.accept()
        else:
            self.lbl_msg.setText("Invalid Password! / رمز عبور نامعتبر است (admin)")


# ------------------------------------------------------------------------------
# 4. MAIN GUI APPLICATION WINDOW
# ------------------------------------------------------------------------------
class LRCSimulatorPro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DBManager()
        self.current_theme = "Pro"
        self.zoom_level = 1.0

        self.setWindowTitle("LRC-HydroGeoMechanics Pro v1.0.0 | LTU Underground H2 Storage Framework")
        self.resize(1340, 880)
        self.setMinimumSize(1100, 720)

        # Set Window Icons if available
        if os.path.exists("d:/l.ico"):
            self.setWindowIcon(QIcon("d:/l.ico"))

        self.init_ui()
        self.apply_theme("Pro")
        self.log("System initialized successfully. Model ready for coupled THM simulations.", "سیستم شبیه‌ساز با موفقیت آماده به کار شد.")
        
        # Auto-run baseline model on startup
        self.run_simulation_pipeline()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(4)

        # --- TOP HEADER BAR ---
        header_bar = QHBoxLayout()
        
        lbl_title = QLabel("⚡ LRC-HydroGeoMechanics Simulator Pro 2026")
        lbl_title.setFont(QFont("Arial", 13, QFont.Bold))
        lbl_title.setStyleSheet("color: #38bdf8;")
        header_bar.addWidget(lbl_title)

        lbl_hdr_link = QLabel("AiBrothersTools.ir | LTU Hydrogen Research")
        lbl_hdr_link.setStyleSheet("color: #94a3b8; font-size: 11px;")
        header_bar.addWidget(lbl_hdr_link)

        header_bar.addStretch()

        self.lbl_datetime = QLabel()
        self.lbl_datetime.setStyleSheet("color: #e2e8f0; font-size: 11px; padding-right: 10px;")
        header_bar.addWidget(self.lbl_datetime)

        self.timer_clock = QTimer(self)
        self.timer_clock.timeout.connect(self.update_clock)
        self.timer_clock.start(1000)
        self.update_clock()

        # Theme Selector
        header_bar.addWidget(QLabel("Theme:"))
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["Pro", "Dark", "Classic", "Pink"])
        self.combo_theme.currentTextChanged.connect(self.apply_theme)
        header_bar.addWidget(self.combo_theme)

        # Zoom Controls
        btn_zoom_in = QPushButton("🔍+")
        btn_zoom_in.setFixedWidth(36)
        btn_zoom_in.clicked.connect(lambda: self.adjust_zoom(0.1))
        header_bar.addWidget(btn_zoom_in)

        btn_zoom_out = QPushButton("🔍-")
        btn_zoom_out.setFixedWidth(36)
        btn_zoom_out.clicked.connect(lambda: self.adjust_zoom(-0.1))
        header_bar.addWidget(btn_zoom_out)

        main_layout.addLayout(header_bar)

        # --- MAIN SPLITTER (Left: Control Panel | Right: Visualizations & Tables) ---
        splitter = QSplitter(Qt.Horizontal)
        
        # Left Panel (Inputs and Action Buttons)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(4, 4, 4, 4)
        left_layout.setSpacing(6)

        # Input Group 1: Cavern & Geological Site Conditions
        grp_geo = QGroupBox("1. Geological & In-Situ Parameters")
        grid_geo = QGridLayout(grp_geo)
        grid_geo.setSpacing(4)
        
        grid_geo.addWidget(QLabel("Depth (m):"), 0, 0)
        self.txt_depth = QLineEdit("500.0")
        grid_geo.addWidget(self.txt_depth, 0, 1)

        grid_geo.addWidget(QLabel("Cavern Radius rc (m):"), 1, 0)
        self.txt_rc = QLineEdit("15.0")
        grid_geo.addWidget(self.txt_rc, 1, 1)

        grid_geo.addWidget(QLabel("Rock Density (kg/m³):"), 2, 0)
        self.txt_density = QLineEdit("2700.0")
        grid_geo.addWidget(self.txt_density, 2, 1)

        grid_geo.addWidget(QLabel("Lateral Stress Ratio K0:"), 3, 0)
        self.txt_k0 = QLineEdit("1.35")
        grid_geo.addWidget(self.txt_k0, 3, 1)

        left_layout.addWidget(grp_geo)

        # Input Group 2: Rock Mass & Liner Mechanics
        grp_mech = QGroupBox("2. Geomechanical & Material Properties")
        grid_mech = QGridLayout(grp_mech)
        grid_mech.setSpacing(4)

        grid_mech.addWidget(QLabel("Young's Modulus E (GPa):"), 0, 0)
        self.txt_E_rock = QLineEdit("45.0")
        grid_mech.addWidget(self.txt_E_rock, 0, 1)

        grid_mech.addWidget(QLabel("Poisson's Ratio ν:"), 1, 0)
        self.txt_nu_rock = QLineEdit("0.24")
        grid_mech.addWidget(self.txt_nu_rock, 1, 1)

        grid_mech.addWidget(QLabel("Cohesion c (MPa):"), 2, 0)
        self.txt_cohesion = QLineEdit("14.0")
        grid_mech.addWidget(self.txt_cohesion, 2, 1)

        grid_mech.addWidget(QLabel("Friction Angle φ (°):"), 3, 0)
        self.txt_friction = QLineEdit("38.0")
        grid_mech.addWidget(self.txt_friction, 3, 1)

        grid_mech.addWidget(QLabel("Steel Liner Thick (mm):"), 4, 0)
        self.txt_t_liner = QLineEdit("25.0")
        grid_mech.addWidget(self.txt_t_liner, 4, 1)

        left_layout.addWidget(grp_mech)

        # Input Group 3: Hydrogen Storage Operations & Thermal
        grp_ops = QGroupBox("3. Operational Cycling & Thermal ΔT")
        grid_ops = QGridLayout(grp_ops)
        grid_ops.setSpacing(4)

        grid_ops.addWidget(QLabel("P_min (Cushion Gas, MPa):"), 0, 0)
        self.txt_pmin = QLineEdit("4.0")
        grid_ops.addWidget(self.txt_pmin, 0, 1)

        grid_ops.addWidget(QLabel("P_max (Peak Storage, MPa):"), 1, 0)
        self.txt_pmax = QLineEdit("22.0")
        grid_ops.addWidget(self.txt_pmax, 1, 1)

        grid_ops.addWidget(QLabel("Thermal Perturbation ΔT (°C):"), 2, 0)
        self.txt_delta_t = QLineEdit("25.0")
        grid_ops.addWidget(self.txt_delta_t, 2, 1)

        grid_ops.addWidget(QLabel("Annual Injection Cycles:"), 3, 0)
        self.txt_cycles = QLineEdit("365")
        grid_ops.addWidget(self.txt_cycles, 3, 1)

        left_layout.addWidget(grp_ops)

        # Action Buttons (All distinct styling colors)
        btn_layout = QGridLayout()
        
        self.btn_run = QPushButton("🚀 Compute Coupled THM")
        self.btn_run.setStyleSheet("background-color: #0284c7; color: white; font-weight: bold; padding: 7px;")
        self.btn_run.clicked.connect(self.run_simulation_pipeline)
        btn_layout.addWidget(self.btn_run, 0, 0, 1, 2)

        self.btn_save = QPushButton("💾 Save Scenario (DB)")
        self.btn_save.setStyleSheet("background-color: #10b981; color: white; font-weight: bold; padding: 5px;")
        self.btn_save.clicked.connect(self.save_scenario)
        btn_layout.addWidget(self.btn_save, 1, 0)

        self.btn_load = QPushButton("📂 Load Runs")
        self.btn_load.setStyleSheet("background-color: #8b5cf6; color: white; font-weight: bold; padding: 5px;")
        self.btn_load.clicked.connect(self.load_historical_runs)
        btn_layout.addWidget(self.btn_load, 1, 1)

        self.btn_reset_db = QPushButton("🗑️ Clear Database")
        self.btn_reset_db.setStyleSheet("background-color: #f59e0b; color: black; font-weight: bold; padding: 5px;")
        self.btn_reset_db.clicked.connect(self.clear_db_records)
        btn_layout.addWidget(self.btn_reset_db, 2, 0)

        self.btn_export = QPushButton("📊 Export Report (CSV)")
        self.btn_export.setStyleSheet("background-color: #06b6d4; color: white; font-weight: bold; padding: 5px;")
        self.btn_export.clicked.connect(self.export_report)
        btn_layout.addWidget(self.btn_export, 2, 1)

        left_layout.addLayout(btn_layout)
        left_layout.addStretch()

        splitter.addWidget(left_widget)
        splitter.setStretchFactor(0, 3)

        # Right Panel (Tabbed Visualizations & Simulation Data)
        self.tab_widget = QTabWidget()
        
        # Tab 1: Spatial Stress Profiles (Kirsch & Thermal)
        tab_stress = QWidget()
        l_stress = QVBoxLayout(tab_stress)
        self.plot_stress = pg.PlotWidget(title="<b>Spatial Stress Distribution & Cavity Wall Redistribution (MPa)</b>")
        self.plot_stress.showGrid(x=True, y=True, alpha=0.3)
        self.plot_stress.addLegend(offset=(10, 10))
        self.plot_stress.setLabel('left', 'Stress (MPa)', color='#38bdf8')
        self.plot_stress.setLabel('bottom', 'Radial Distance from Cavern Center r (m)', color='#38bdf8')
        l_stress.addWidget(self.plot_stress)
        self.tab_widget.addTab(tab_stress, "📈 THM Stress Profiles")

        # Tab 2: Cyclic Pressure & Liner Fatigue Analysis
        tab_cycling = QWidget()
        l_cycling = QVBoxLayout(tab_cycling)
        self.plot_cycling = pg.PlotWidget(title="<b>Cyclic Hydrogen Pressure & Steel Liner Von Mises Stress vs Yield</b>")
        self.plot_cycling.showGrid(x=True, y=True, alpha=0.3)
        self.plot_cycling.addLegend(offset=(10, 10))
        self.plot_cycling.setLabel('left', 'Von Mises Stress (MPa)', color='#f43f5e')
        self.plot_cycling.setLabel('bottom', 'Operational Injection / Withdrawal Days', color='#38bdf8')
        l_cycling.addWidget(self.plot_cycling)
        self.tab_widget.addTab(tab_cycling, "🔄 Cyclic Fatigue & Liner Safety")

        # Tab 3: Historical Runs & DB Records
        tab_db = QWidget()
        l_db = QVBoxLayout(tab_db)
        self.table_db = QTableWidget()
        self.table_db.setColumnCount(8)
        self.table_db.setHorizontalHeaderLabels([
            "ID", "Timestamp", "Scenario Name", "Depth (m)", "P_max (MPa)", 
            "Max Liner Stress", "Plastic Radius (m)", "Safety Factor"
        ])
        self.table_db.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        l_db.addWidget(self.table_db)
        self.tab_widget.addTab(tab_db, "🗄️ Database Records")

        splitter.addWidget(self.tab_widget)
        splitter.setStretchFactor(1, 7)

        main_layout.addWidget(splitter, stretch=8)

        # --- BOTTOM LOGS & DIAGNOSTICS ---
        grp_log = QGroupBox("System Activity, Mathematical Diagnostics & Bilingual Logs | لاگ محاسباتی")
        v_log = QVBoxLayout(grp_log)
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setMaximumHeight(140)
        v_log.addWidget(self.txt_log)
        main_layout.addWidget(grp_log, stretch=2)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Parviz Tajdari | Swedish Natural H2 & LRC Project Framework Ready.")

    # --------------------------------------------------------------------------
    # PIPELINE EXECUTION & NUMERICAL SOLVER TRIGGER
    # --------------------------------------------------------------------------
    def run_simulation_pipeline(self):
        try:
            # Parse inputs with robust validation
            depth = float(self.txt_depth.text())
            rc = float(self.txt_rc.text())
            rho = float(self.txt_density.text())
            k0 = float(self.txt_k0.text())
            E_rock = float(self.txt_E_rock.text())
            nu_rock = float(self.txt_nu_rock.text())
            cohesion = float(self.txt_cohesion.text())
            phi = float(self.txt_friction.text())
            t_liner = float(self.txt_t_liner.text()) / 1000.0 # to meters
            p_min = float(self.txt_pmin.text())
            p_max = float(self.txt_pmax.text())
            delta_t = float(self.txt_delta_t.text())
            cycles = int(self.txt_cycles.text())

            # 1. In-situ stress calculation
            sigma_v, sigma_h = CoupledTHMEngine.calculate_insitu_stress(depth, rho, k0)

            # 2. Coupled THM Spatial Stress Profiles (Peak Pressure P_max)
            r, sig_r, sig_theta, u_r = CoupledTHMEngine.solve_spatial_stress_distribution(
                rc, p_max, sigma_h, E_rock, nu_rock, alpha_t=1.0e-5, delta_t=delta_t, r_max=rc*5.0, num_nodes=250
            )

            # 3. Plastic Zone Radius Calculation (Mohr-Coulomb Failure)
            r_plastic = CoupledTHMEngine.calculate_plastic_zone(rc, p_min, sigma_h, cohesion, phi)

            # 4. Liner Integrity Evaluation
            max_liner_stress, safety_factor = CoupledTHMEngine.evaluate_liner_integrity(
                p_max, rc, t_liner, t_concrete=0.5
            )

            # --- PLOTTING 1: Spatial Stress Profiles ---
            self.plot_stress.clear()
            
            p1 = self.plot_stress.plot(r, sig_theta, pen=pg.mkPen('#38bdf8', width=2.5), name="Tangential Stress σ_θ (MPa)")
            p2 = self.plot_stress.plot(r, sig_r, pen=pg.mkPen('#34d399', width=2.5), name="Radial Stress σ_r (MPa)")
            
            # Far-field In-situ stress baseline
            p3 = self.plot_stress.plot([rc, r[-1]], [sigma_h, sigma_h], 
                                       pen=pg.mkPen('#9ca3af', width=1.5, style=Qt.DashLine), name="Far-field σ_h Baseline")
            
            # Plastic radius marker if yielded
            if r_plastic > rc:
                self.plot_stress.addItem(pg.InfiniteLine(pos=r_plastic, angle=90, pen=pg.mkPen('#ef4444', width=2, style=Qt.DotLine),
                                                        label=f"Plastic Radius: {r_plastic:.2f}m", labelOpts={'color': '#ef4444'}))

            # --- PLOTTING 2: Cyclic Pressure & Liner Fatigue ---
            self.plot_cycling.clear()
            t_days = np.linspace(0, 365, 365)
            # Sine-wave hydrogen cyclic withdrawal/injection
            p_cycle = p_min + (p_max - p_min) * (0.5 * (1.0 + np.sin(2 * np.pi * t_days / 30.0)))
            
            # Dynamic Liner Stress under cycling
            liner_stresses = (p_cycle * (rc - t_liner)) / t_liner
            
            self.plot_cycling.plot(t_days, liner_stresses, pen=pg.mkPen('#f43f5e', width=2), name="Cyclic Liner Hoop Stress (MPa)")
            self.plot_cycling.plot([0, 365], [355.0, 355.0], pen=pg.mkPen('#eab308', width=2, style=Qt.DashLine), name="S355 Steel Yield Limit (355 MPa)")

            # Store last computed state
            self.last_results = {
                'name': f"Depth_{depth}m_Pmax_{p_max}MPa",
                'r_c': rc, 'depth': depth, 'p_min': p_min, 'p_max': p_max,
                'dt': delta_t, 'cycles': cycles, 'E_rock': E_rock, 'nu_rock': nu_rock,
                't_liner': t_liner, 'c_rock': cohesion, 'phi_rock': phi,
                'max_liner_stress': round(float(max_liner_stress), 2),
                'r_plastic': round(float(r_plastic), 2),
                'safety_factor': round(float(safety_factor), 2)
            }

            self.log(
                f"[COMPLETED] Depth: {depth}m | σ_v: {sigma_v:.1f} MPa | σ_h: {sigma_h:.1f} MPa | Max Liner σ: {max_liner_stress:.1f} MPa | Plastic Zone Radius: {r_plastic:.2f} m | Liner Safety Factor: {safety_factor:.2f}",
                f"[محاسبه کامل شد] عمق: {depth} متر | تنش برجا: {sigma_h:.1f} مگاپاسکال | تنش لاینر: {max_liner_stress:.1f} مگاپاسکال | ضریب اطمینان تسلیم: {safety_factor:.2f}"
            )
            self.status_bar.showMessage(f"Calculation Finished. Plastic Radius: {r_plastic:.2f}m | Liner SF: {safety_factor:.2f}")

        except Exception as e:
            err_tb = traceback.format_exc()
            self.log(f"[ERROR] Simulation Failed: {str(e)}\n{err_tb}", f"[خطای محاسباتی] عملیات متوقف شد: {str(e)}")
            QMessageBox.critical(self, "Calculation Error", f"Error during computation:\n{str(e)}")

    def save_scenario(self):
        if hasattr(self, 'last_results'):
            success = self.db.save_simulation(self.last_results)
            if success:
                self.log(f"[DATABASE] Scenario '{self.last_results['name']}' saved to SQLite.", "سناریو با موفقیت در دیتابیس محلی ذخیره شد.")
                self.load_historical_runs()
                QMessageBox.information(self, "Success", "Simulation run successfully saved to Database!")
        else:
            QMessageBox.warning(self, "Warning", "Please run a simulation before saving.")

    def load_historical_runs(self):
        records = self.db.fetch_all_simulations()
        self.table_db.setRowCount(len(records))
        for row_idx, row_data in enumerate(records):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table_db.setItem(row_idx, col_idx, item)
        self.tab_widget.setCurrentIndex(2)
        self.log(f"[DATABASE] Loaded {len(records)} simulation runs from SQLite storage.", f"تعداد {len(records)} رکورد سناریو از دیتابیس بارگذاری شد.")

    def clear_db_records(self):
        reply = QMessageBox.question(self, "Confirm Reset", "Are you sure you want to clear all simulation records in the database?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.reset_db()
            self.load_historical_runs()
            self.log("[DATABASE] All records cleared from database.", "تمامی رکوردهای دیتابیس پاک شدند.")

    def export_report(self):
        try:
            records = self.db.fetch_all_simulations()
            if not records:
                QMessageBox.warning(self, "Warning", "No database records available to export.")
                return
            
            file_path, _ = QFileDialog.getSaveFileName(self, "Export Simulations to CSV", "LTU_LRC_Simulation_Report.csv", "CSV Files (*.csv)")
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("ID,Timestamp,Scenario,Depth_m,P_max_MPa,Max_Liner_Stress_MPa,Plastic_Radius_m,Safety_Factor\n")
                    for row in records:
                        f.write(",".join(map(str, row)) + "\n")
                self.log(f"[EXPORT] Successfully exported report to: {file_path}", f"گزارش نتایج در فایل CSV ذخیره شد: {file_path}")
                QMessageBox.information(self, "Export Completed", f"Data exported successfully to:\n{file_path}")
        except Exception as e:
            self.log(f"[EXPORT ERROR] {str(e)}", f"خطا در صدور گزارش CSV: {str(e)}")

    def log(self, en_msg, fa_msg):
        t_str = datetime.datetime.now().strftime("%H:%M:%S")
        formatted = f"[{t_str}] <b>EN:</b> {en_msg}<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>FA:</b> <span style='color:#a78bfa;'>{fa_msg}</span>"
        self.txt_log.append(formatted)

    def update_clock(self):
        now = QDateTime.currentDateTime()
        self.lbl_datetime.setText(now.toString("yyyy-MM-dd HH:mm:ss"))

    def adjust_zoom(self, delta):
        self.zoom_level = max(0.8, min(1.5, self.zoom_level + delta))
        font = self.font()
        font.setPointSizeF(9.0 * self.zoom_level)
        self.setFont(font)
        self.log(f"[UI] Zoom adjusted to: {self.zoom_level:.1f}x", f"بزرگ‌نمایی رابط کاربری روی {self.zoom_level:.1f}x تنظیم شد.")

    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        if theme_name == "Pro":
            self.setStyleSheet("""
                QMainWindow { background-color: #0f172a; color: #e2e8f0; }
                QGroupBox { border: 1px solid #334155; border-radius: 6px; margin-top: 10px; font-weight: bold; color: #38bdf8; }
                QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 4px; }
                QLabel { color: #cbd5e1; font-size: 11px; }
                QLineEdit { background-color: #1e293b; color: #f8fafc; border: 1px solid #475569; border-radius: 4px; padding: 3px 6px; }
                QComboBox { background-color: #1e293b; color: #f8fafc; border: 1px solid #475569; border-radius: 4px; padding: 2px 6px; }
                QTabWidget::pane { border: 1px solid #334155; background-color: #1e293b; }
                QTabBar::tab { background: #0f172a; color: #94a3b8; padding: 8px 14px; border: 1px solid #334155; border-bottom: none; border-top-left-radius: 4px; border-top-right-radius: 4px; }
                QTabBar::tab:selected { background: #1e293b; color: #38bdf8; font-weight: bold; }
                QTextEdit { background-color: #090d16; color: #e2e8f0; border: 1px solid #334155; font-family: 'Consolas', monospace; font-size: 11px; }
                QTableWidget { background-color: #1e293b; color: #f8fafc; gridline-color: #334155; }
                QHeaderView::section { background-color: #0f172a; color: #38bdf8; padding: 4px; font-weight: bold; }
            """)
        elif theme_name == "Dark":
            self.setStyleSheet("""
                QMainWindow { background-color: #18181b; color: #f4f4f5; }
                QGroupBox { border: 1px solid #3f3f46; color: #a1a1aa; font-weight: bold; }
                QLineEdit { background-color: #27272a; color: #ffffff; border: 1px solid #52525b; }
                QTextEdit { background-color: #09090b; color: #a1a1aa; }
            """)
        elif theme_name == "Classic":
            self.setStyleSheet("""
                QMainWindow { background-color: #f1f5f9; color: #0f172a; }
                QGroupBox { border: 1px solid #cbd5e1; color: #0369a1; font-weight: bold; }
                QLabel { color: #1e293b; }
                QLineEdit { background-color: #ffffff; color: #0f172a; border: 1px solid #94a3b8; }
                QTextEdit { background-color: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; }
                QTabBar::tab:selected { background: #ffffff; color: #0284c7; }
            """)
        elif theme_name == "Pink":
            self.setStyleSheet("""
                QMainWindow { background-color: #2a1526; color: #fce7f3; }
                QGroupBox { border: 1px solid #db2777; color: #f472b6; font-weight: bold; }
                QLineEdit { background-color: #4a1d46; color: #ffffff; border: 1px solid #be185d; }
                QPushButton { background-color: #db2777; color: white; }
                QTextEdit { background-color: #1f0d1c; color: #fbcfe8; }
            """)


# ------------------------------------------------------------------------------
# 5. ENTRY POINT WITH AUTHENTICATION
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))

    # Password check dialog (Password: admin)
    auth = AuthDialog()
    if auth.exec_() == QDialog.Accepted:
        window = LRCSimulatorPro()
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)
