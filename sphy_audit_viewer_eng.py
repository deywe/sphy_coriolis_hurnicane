from ursina import *
import pandas as pd
import numpy as np
import hashlib

# Full HD Window Configuration for Pop!_OS / Linux
# Using Harpia Audit System - Phase Integrity Protocol
app = Ursina(title="Harpia Audit - Phase Integrity System", size=(1920, 1080))
window.color = color.black
window.vsync = True

# --- DATASET LOADING ---
try:
    print("📥 Loading Signed Parquet Dataset...")
    df = pd.read_parquet("sphy_audit_data.parquet")
    num_frames = df['frame'].max() + 1
    particles_per_frame = len(df) // num_frames
except Exception as e:
    print(f"❌ Error: Ensure the file 'sphy_audit_data.parquet' exists in the directory.\n{e}")
    exit()

# --- RENDERING ENTITY ---
cloud_entity = Entity(
    model=Mesh(
        vertices=[(0,0,0)] * particles_per_frame,
        colors=[color.cyan for _ in range(particles_per_frame)],
        mode='point',
        thickness=0.015
    ),
    texture='particle',
    unlit=True,
    transparent=True
)

# --- COMMAND INTERFACE (HUD) ---
audit_status = Text(text="AUDIT: STANDBY", position=(-0.85, 0.45), scale=1.2)
hash_display = Text(text="HASH: NULL", position=(-0.85, 0.40), scale=0.7, color=color.gray)
frame_info = Text(text="FRAME: 0", position=(-0.85, 0.35), scale=1, color=color.yellow)

# On-Screen Control Labels
Text(text="AUDIT CONTROLS:", position=(0.5, 0.45), color=color.gold, scale=0.8)
Text(text="[LEFT CLICK]: Drag (Pan)", position=(0.5, 0.41), scale=0.7)
Text(text="[RIGHT CLICK]: Rotate (Orbit)", position=(0.5, 0.38), scale=0.7)
Text(text="[MOUSE WHEEL]: Zoom In/Out", position=(0.5, 0.35), scale=0.7)
Text(text="[KEY R]: Reset Camera", position=(0.5, 0.32), scale=0.7)

current_frame = 0

def update():
    global current_frame
    
    # Selecting data for the current frame
    frame_data = df[df['frame'] == current_frame]
    pos = frame_data[['x', 'y', 'z']].values
    
    # --- SHA-256 CRYPTOGRAPHIC VALIDATION ---
    # Converts positions to bytes to verify the SPHY integrity hash
    current_bytes = pos.astype(np.float32).tobytes()
    calculated_hash = hashlib.sha256(current_bytes).hexdigest()
    original_hash = frame_data['hash'].iloc[0]
    
    if calculated_hash == original_hash:
        audit_status.text = "AUDIT: VERIFIED [OK]"
        audit_status.color = color.green
    else:
        audit_status.text = "AUDIT: TAMPERED [FAIL]"
        audit_status.color = color.red
        
    hash_display.text = f"SHA256: {calculated_hash}"
    frame_info.text = f"FRAME: {current_frame} / {num_frames-1}"
    
    # Update Mesh with Zero-Point brightness filter
    cloud_entity.model.vertices = pos.tolist()
    # Logic to highlight particles based on Z-axis phase
    cloud_entity.model.colors = [color.hsv(190, 0.8, 1 if p[2] > 1.5 else 0.4) for p in pos]
    cloud_entity.model.generate()
    
    current_frame = (current_frame + 1) % num_frames

# --- CAMERA AND INPUT CONFIGURATION ---
camera.position = (0, 80, -350)
ec = EditorCamera()

# Control remapping for improved navigation on Pop!_OS/Linux hardware
ec.pan_button = 'left mouse'       # Pan on left click
ec.rotation_button = 'right mouse' # Orbit on right click
ec.rotation_speed = 60
ec.pan_speed = (15, 15)

def input(key):
    if key == 'r':
        camera.position = (0, 80, -350)
        camera.rotation = (0, 0, 0)

app.run()
