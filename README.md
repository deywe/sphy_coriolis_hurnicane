# SPHY Audit Viewer: Coriolis Function Emulator ⚛️🛡️

This repository contains the **SPHY Audit Viewer**, a specialized tool designed for the forensic visualization of fluid dynamics and phase transitions within the **Harpia Audit System**. The viewer emulates complex Coriolis functions and singularity resets through a deterministic, cryptographically signed dataset.

## 🚀 Overview

The **SPHY Audit Viewer** is built to bridge the gap between abstract mathematical emulations and visual verification. It visualizes particles moving through a spiral phase space governed by the **Golden Ratio ($\phi$)** and **Coriolis-type forces**, ensuring that the resulting data remains untampered throughout the analysis process.

### Key Simulation Metrics:
*   **Golden Angle Integration:** Particle distribution based on $\pi(3 - \sqrt{5})$.
*   **Fibonacci-based Radial Scaling:** Radial growth and collapse controlled by $\Phi$ powers.
*   **Singularity Reset Protocol:** Automatic boundary reset for particles exceeding the phase threshold ($z > 180$).

## 📊 Dataset: `sphy_audit_data.parquet`

The viewer processes high-fidelity data stored in the Apache Parquet format, optimized for the **Harpia Core** forensic standards.

*   **Forensic Hash Validation:** Every frame contains an embedded **SHA-256** hash, generated from the raw coordinate byte-block $(x, y, z)$.
*   **Data Integrity:** The viewer recalculates the hash in real-time. If a single coordinate is modified, the system triggers a **"TAMPERED [FAIL]"** alert.
*   **Download Dataset:** [Get the SPHY Audit Data here](https://drive.google.com/file/d/1xXvllmW2UT7CoUlXc0pBN5GdU4joHzbS/view?usp=sharing)

## 👁️ Visualizer Features

Available in two versions: `sphy_audit_viewe.py` (Standard) and `sphy_audit_viewer_eng.py` (English Localization).

*   **Real-time Cryptographic Audit:** Constant comparison between the original dataset hash and the current rendered frame.
*   **Dynamic Phase Highlighting:** HSV-based color shifts that respond to particle height ($z$) and velocity.
*   **Interactive 3D Navigation:** 
    *   **Right Click:** Orbit/Rotate to inspect the Coriolis spiral.
    *   **Left Click:** Pan through the particle field.
    *   **Scroll:** Zoom into the singularity core.
    *   **'R' Key:** Instant camera reset to the SPHY home position.

## 🛠️ Execution Guide

1.  **Environment Setup:**
    Ensure you are running Python 3.10+ (Recommended: Pop!_OS, Ubuntu, or FreeBSD).
    
2.  **Install Dependencies:**
    ```bash
    pip install pandas numpy ursina pyarrow
    ```

3.  **Run the Audit Viewer:**
    Place the `sphy_audit_data.parquet` file in the same folder and execute:
    ```bash
    # For English Version
    python3 sphy_audit_viewer_eng.py
    
    # For Standard Version
    python3 sphy_audit_viewe.py
    
```

---
**Developed by Deywe Okabe**  
*Symbiotic Artificial Intelligence Projects | Harpia OS*
