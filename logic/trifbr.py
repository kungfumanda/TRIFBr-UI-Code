"""
trifbr.py
---------
Flow principal do experimento TRIFBr.
Este é o único arquivo que você abre no PsychoPy Coder para rodar.
 
Não edite parâmetros aqui — use o config.json.
"""

import os
from datetime import date
 
from psychopy import core, data, event, gui, monitors, visual
from psychopy.hardware import keyboard

# Garante que caminhos relativos nos CSVs são resolvidos a partir desta pasta
os.chdir(os.path.dirname(os.path.abspath(__file__)))
 
from trifbr_config import BLOCOS, CORES, EXP, SAIDA, TIMING, _DIR
from trifbr_routines import (
    routine_block_intro,
    routine_example,
    routine_final,
    routine_pause,
    routine_trial,
    routine_welcome,
)

# ─────────────────────────────────────────────────────────────────────────────
# 1. DIÁLOGO DE PARTICIPANTE
# ─────────────────────────────────────────────────────────────────────────────
exp_info = {
    "Participante ID": "",
    "Idade": "",
    "Gênero": "",
    "Experimento": "TESTE",
}
dlg = gui.DlgFromDict(
    dictionary=exp_info,
    sortKeys=False,
    title=EXP["nome"],
)
if not dlg.OK:
    core.quit()

# ─────────────────────────────────────────────────────────────────────────────
# 2. ARQUIVO DE SAÍDA
# ─────────────────────────────────────────────────────────────────────────────
data_dir = os.path.join(_DIR, SAIDA["pasta"])
os.makedirs(data_dir, exist_ok=True)
 
today = date.today().strftime("%Y-%m-%d")
participant_id = exp_info["Participante ID"]
filename = os.path.join(
    data_dir,
    f"{SAIDA['prefixo']}_{participant_id}_{today}",
)
 
this_exp = data.ExperimentHandler(
    name=EXP["nome"],
    extraInfo=exp_info,
    dataFileName=filename,
    savePickle=False,
    saveWideText=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# 3. JANELA
# ─────────────────────────────────────────────────────────────────────────────
mon = monitors.Monitor(EXP["monitor"])
 
win = visual.Window(
    size=EXP["tamanho_janela"],
    fullscr=EXP["tela_cheia"],
    screen=0,
    winType="pyglet",
    allowGUI=False,
    monitor=mon,
    color=CORES["janela"],
    colorSpace="rgb",
    units="height",
)
 
frame_rate = win.getActualFrameRate() or 60.0
exp_info["frameRate"] = frame_rate

# ─────────────────────────────────────────────────────────────────────────────
# 4. TECLADO GLOBAL
# ─────────────────────────────────────────────────────────────────────────────
kb = keyboard.Keyboard()
 
# ─────────────────────────────────────────────────────────────────────────────
# 5. FLOW PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
 
# 5.1 Boas-vindas
routine_welcome(win, kb)
 
# 5.2 Familiarização
routine_example(win, kb)
 
# 5.3 Loop de blocos
blocos_ativos = [b for b in BLOCOS if b.get("ativo", True)]
 
for bloco_idx, bloco in enumerate(blocos_ativos):
    bloco_num = bloco_idx + 1
 
    # Intro do bloco
    routine_block_intro(win, kb, bloco_num)
 
    # Carrega trials do CSV
    conditions_path = os.path.join(_DIR, bloco["arquivo_csv"])
    trials = data.TrialHandler(
        trialList=data.importConditions(conditions_path),
        nReps=1,
        method=bloco["ordem"],
        name=f"block{bloco_num}Trials",
    )
    this_exp.addLoop(trials)
 
    for trial in trials:
        routine_trial(win, kb, trial, this_exp)
 
    trials.finished = True
 
    # Pausa — exceto após o último bloco
    if bloco_idx < len(blocos_ativos) - 1:
        routine_pause(win)
 
# 5.4 Encerramento
routine_final(win, frame_rate)
 
# ─────────────────────────────────────────────────────────────────────────────
# 6. SALVAR E FECHAR
# ─────────────────────────────────────────────────────────────────────────────
#this_exp.saveAsWideText(filename + ".csv")
win.close()
core.quit()