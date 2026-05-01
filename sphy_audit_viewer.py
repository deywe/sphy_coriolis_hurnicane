from ursina import *
import pandas as pd
import numpy as np
import hashlib

# Configuração de Janela Full HD para o Pop!_OS
app = Ursina(title="Harpia Audit - Sistema de Integridade de Fase", size=(1920, 1080))
window.color = color.black
window.vsync = True

# --- CARREGAR DATASET ---
try:
    print("📥 Carregando Dataset Parquet assinado...")
    df = pd.read_parquet("sphy_audit_data.parquet")
    num_frames = df['frame'].max() + 1
    particles_per_frame = len(df) // num_frames
except Exception as e:
    print(f"❌ Erro: Certifique-se de que o arquivo 'sphy_audit_data.parquet' existe.\n{e}")
    exit()

# --- ENTIDADE DE RENDERIZAÇÃO ---
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

# --- INTERFACE DE COMANDO (HUD) ---
audit_status = Text(text="AUDIT: STANDBY", position=(-0.85, 0.45), scale=1.2)
hash_display = Text(text="HASH: NULL", position=(-0.85, 0.40), scale=0.7, color=color.gray)
frame_info = Text(text="FRAME: 0", position=(-0.85, 0.35), scale=1, color=color.yellow)

# Lista de Funções na Tela
Text(text="CONTROLES DE AUDITORIA:", position=(0.5, 0.45), color=color.gold, scale=0.8)
Text(text="[BOTAO ESQUERDO]: Arrastar (Pan)", position=(0.5, 0.41), scale=0.7)
Text(text="[BOTAO DIREITO]: Rotacionar (Orbit)", position=(0.5, 0.38), scale=0.7)
Text(text="[SCROLL MOUSE]: Aproximar (Zoom)", position=(0.5, 0.35), scale=0.7)
Text(text="[TECLA R]: Resetar Câmera", position=(0.5, 0.32), scale=0.7)

current_frame = 0

def update():
    global current_frame
    
    # Seleção de dados do frame atual
    frame_data = df[df['frame'] == current_frame]
    pos = frame_data[['x', 'y', 'z']].values
    
    # --- VALIDAÇÃO CRIPTOGRÁFICA SHA-256 ---
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
    
    # Atualização da Mesh com filtro de brilho para o Ponto Zero
    cloud_entity.model.vertices = pos.tolist()
    cloud_entity.model.colors = [color.hsv(190, 0.8, 1 if p[2] > 1.5 else 0) for p in pos]
    cloud_entity.model.generate()
    
    current_frame = (current_frame + 1) % num_frames

# --- CONFIGURAÇÃO DE CÂMERA E INPUTS ---
camera.position = (0, 80, -350)
ec = EditorCamera()

# Mapeamento para contornar problemas de hardware (Botão do Meio)
ec.pan_button = 'left mouse'      # Pan no esquerdo
ec.rotation_button = 'right mouse' # Rotação habilitada no direito
ec.rotation_speed = 60
ec.pan_speed = (15, 15)

def input(key):
    if key == 'r':
        camera.position = (0, 80, -350)
        camera.rotation = (0, 0, 0)

app.run()
