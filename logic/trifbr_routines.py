"""
trifbr_routines.py
------------------
Define todas as rotinas do experimento TRIFBr.
Importa configuração de trifbr_config.py — não edite valores aqui,
edite o config.json.
 
Rotinas disponíveis:
    routine_welcome(win, kb)
    routine_example(win, kb)
    routine_block_intro(win, kb, bloco_num)
    routine_trial(win, kb, trial_data, this_exp)
    routine_pause(win)
    routine_final(win, frame_rate)
"""

from psychopy import core, data, event, visual
 
from trifbr_config import (
    BLOCOS, CORES, IMAGE_POS, IMAGE_SIZE, TIMING, TREINO, TXT,
    VIDEO_POS, VIDEO_SIZE, _DIR,
)
 
import os

# ─────────────────────────────────────────────────────────────────────────────
# Helpers internos
# ─────────────────────────────────────────────────────────────────────────────
 
def _wait_advance(win, kb, mouse):
    """Aguarda espaço ou clique esquerdo. Sai do experimento se Escape."""
    mouse.clickReset()
    kb.clearEvents(eventType="keyboard")
    while True:
        keys = kb.getKeys(keyList=["space", "escape"])
        if keys:
            if keys[0].name == "escape":
                win.close()
                core.quit()
            return
        if mouse.getPressed()[0]:
            return
        win.flip()
 
 
def _make_image_stims(win, image_paths, names=None):
    """Cria lista de 4 ImageStim a partir de uma lista de caminhos."""
    stims = []
    for i, path in enumerate(image_paths):
        name = names[i] if names else f"stim_image_{i+1}"
        stims.append(
            visual.ImageStim(
                win, image=path,
                pos=IMAGE_POS[i], size=IMAGE_SIZE,
                units="height", name=name,
            )
        )
    return stims
 
 
def _make_number_labels(win):
    """Cria os rótulos 1–4 abaixo de cada imagem de resposta."""
    return [
        visual.TextStim(
            win, text=str(i + 1),
            pos=(IMAGE_POS[i][0], IMAGE_POS[i][1] - IMAGE_SIZE[1] / 2 - 0.03),
            height=0.04, color=CORES["texto"], units="height",
        )
        for i in range(4)
    ]
 
 # ─────────────────────────────────────────────────────────────────────────────
# 1. Boas-vindas
# ─────────────────────────────────────────────────────────────────────────────
 
def routine_welcome(win, kb):
    """Tela de boas-vindas com título, corpo e instrução de avanço."""
    title = visual.TextStim(
        win, text=TXT["welcome_titulo"],
        pos=(0, 0.32), height=0.055,
        wrapWidth=1.4, color=CORES["texto"], bold=True,
    )
    body = visual.TextStim(
        win, text=TXT["welcome_corpo"],
        pos=(0, 0.02), height=0.038,
        wrapWidth=1.4, color=CORES["texto"],
    )
    advance = visual.TextStim(
        win, text=TXT["welcome_avanco"],
        pos=(0, -0.38), height=0.033,
        wrapWidth=1.4, color=CORES["texto"], italic=True,
    )
    mouse = event.Mouse(visible=True,win=win)
    
    while True:
        title.draw()
        body.draw()
        advance.draw()
        win.flip()

        keys = kb.getKeys(keyList=["space", "escape"])
        if keys:
            if keys[0].name == "escape":
                win.close()
                core.quit()
            break
        if mouse.getPressed()[0]:
            break
 
 
# ─────────────────────────────────────────────────────────────────────────────
# 2. Exemplo / familiarização
# ─────────────────────────────────────────────────────────────────────────────
 
def routine_example(win, kb):
    """
    Roda os trials do CSV de treino sem salvar dados e sem feedback.
    O vídeo fica em loop e as imagens aparecem juntas desde o início,
    igual ao trial principal.
    """
    conditions_path = os.path.join(_DIR, TREINO["arquivo_csv"])
    trials = data.TrialHandler(
        trialList=data.importConditions(conditions_path),
        nReps=1,
        method="sequential",
        name="treinoBT",
    )
 
    titulo = visual.TextStim(
        win, text=TXT["exemplo_titulo"],
        pos=(0, 0.46), height=0.042,
        color=CORES["texto"], bold=True,
    )
    continuar = visual.TextStim(
        win, text=TXT["exemplo_continuar"],
        pos=(0, -0.46), height=0.033,
        color=CORES["texto"], italic=True,
    )
 
    mouse = event.Mouse(visible=True,win=win)
 
    for trial in trials:
        # Estímulos do trial de treino
        video = visual.MovieStim(
            win, filename=trial["Target_Video"],
            pos=VIDEO_POS, size=VIDEO_SIZE,
            units="height", loop=True, noAudio=True,
        )
        image_paths = [trial[f"Image_{i}"] for i in range(1, 5)]
        images = _make_image_stims(win, image_paths)
        labels = _make_number_labels(win)
 
        mouse.clickReset()
        kb.clearEvents()
        video.play()
        responded = False
 
        while not responded:
            titulo.draw()
            video.draw()
            for img in images:
                img.draw()
            for lbl in labels:
                lbl.draw()
            continuar.draw()
            win.flip()
 
            # Teclado
            keys = kb.getKeys(keyList=["1", "2", "3", "4", "escape"])
            if keys:
                if keys[0].name == "escape":
                    video.stop()
                    win.close()
                    core.quit()
                responded = True
 
            # Mouse
            if not responded and mouse.getPressed()[0]:
                for img in images:
                    if mouse.isPressedIn(img):
                        responded = True
                        break
 
        video.stop()
 
 
# ─────────────────────────────────────────────────────────────────────────────
# 3. Intro de bloco (genérica)
# ─────────────────────────────────────────────────────────────────────────────
 
def routine_block_intro(win, kb, bloco_num):
    """
    Tela de início de bloco genérica.
    bloco_num : int, 1-indexado
    """
    numero = visual.TextStim(
        win,
        text=f"BLOCO {bloco_num}",
        pos=(0, 0.10), height=0.07,
        color=CORES["texto"], bold=True,
    )
    continuar = visual.TextStim(
        win, text=TXT["bloco_continuar"],
        pos=(0, -0.15), height=0.035,
        wrapWidth=1.4, color=CORES["texto"], italic=True,
    )
    mouse = event.Mouse(visible=True,win=win)
 
    while True:
        numero.draw()
        continuar.draw()
        win.flip()
        
        keys = kb.getKeys(keyList=["space", "escape"])
        if keys:
            if keys[0].name == "escape":
                win.close()
                core.quit()
            break
        if mouse.getPressed()[0]:
            break
 
# ─────────────────────────────────────────────────────────────────────────────
# 4. Trial principal
# ─────────────────────────────────────────────────────────────────────────────
 
def routine_trial(win, kb, trial_data, this_exp):
    """
    Um trial completo de reconhecimento de identidade.
    Vídeo em loop + 4 imagens aparecem simultaneamente.
    Termina apenas por resposta (mouse ou teclado).
 
    Lógica de scoring preservada do Builder original.
    """
    # ── Identificação do trial (preservado do Builder) ──
    identificator      = trial_data["Bloco"] + trial_data["Lamina_ID"]
    correct_pos        = str(trial_data["Target_Correto_Posicao"])
    correct_response_name = "stim_image_" + correct_pos
 
    # ── Estímulos ──
    video = visual.MovieStim(
        win, filename=trial_data["Target_Video"],
        pos=VIDEO_POS, size=VIDEO_SIZE,
        units="height", loop=True, noAudio=True,
    )
 
    image_paths = [trial_data[f"Image_{i}"] for i in range(1, 5)]
    image_names = [f"stim_image_{i}" for i in range(1, 5)]
    images = _make_image_stims(win, image_paths, names=image_names)
    labels = _make_number_labels(win)
 
    # ── Variáveis de resposta ──
    is_correct        = 0
    rt_value          = None
    response_method   = "miss"
    selected_option   = None
 
    mouse = event.Mouse(visible=True,win=win)
    mouse.clickReset()
    kb.clearEvents()
    trial_clock = core.Clock()
 
    video.play()
 
    while True:
        video.draw()
        for img in images:
            img.draw()
        for lbl in labels:
            lbl.draw()
        win.flip()
 
        # ── Teclado ──
        keys = kb.getKeys(keyList=["1", "2", "3", "4", "escape"])
        if keys:
            if keys[0].name == "escape":
                video.stop()
                win.close()
                core.quit()
            response_method = "keyboard"
            rt_value        = keys[0].rt
            selected_option = keys[0].name
            if selected_option == correct_pos:
                is_correct = 1
            break
 
        # ── Mouse ──
        if mouse.getPressed()[0]:
            for img in images:
                if mouse.isPressedIn(img):
                    response_method = "mouse"
                    _, times        = mouse.getPressed(getTime=True)
                    rt_value        = times[0] if times[0] else trial_clock.getTime()
                    selected_option = img.name
                    if selected_option == correct_response_name:
                        is_correct = 1
                    break
            if selected_option is not None:
                break
 
    video.stop()
 
    # ── Salvar dados (preservado do Builder original) ──
    this_exp.addData("ANALYSIS_Lamina_ID",        identificator)
    this_exp.addData("ANALYSIS_CR",               is_correct)
    this_exp.addData("ANALYSIS_RT",               round(rt_value, 3) if rt_value is not None else None)
    this_exp.addData("ANALYSIS_Response_Method",  response_method)
    this_exp.addData("ANALYSIS_Selected_Option",  selected_option)
    this_exp.addData("ANALYSIS_Target_Component", correct_response_name)
    this_exp.nextEntry()
 
 
# ─────────────────────────────────────────────────────────────────────────────
# 5. Pausa entre blocos
# ─────────────────────────────────────────────────────────────────────────────
 
def routine_pause(win):
    """Pausa automática entre blocos — duração definida no config.json."""
    win.flip()
    core.wait(TIMING["pausa_entre_blocos_seg"])
 
 
# ─────────────────────────────────────────────────────────────────────────────
# 6. Encerramento
# ─────────────────────────────────────────────────────────────────────────────
 
def routine_final(win, frame_rate):
    """Tela de encerramento — duração definida no config.json."""
    msg = visual.TextStim(
        win, text=TXT["encerramento"],
        pos=(0, 0), height=0.06,
        color=CORES["texto"], bold=True,
    )
    n_frames = int(TIMING["tela_final_seg"] * frame_rate)
    for _ in range(n_frames):
        msg.draw()
        win.flip()