"""
trifbr_config.py
----------------
Carrega o config.json e expõe as variáveis para os demais módulos.
Este arquivo não deve ser editado — todas as mudanças vão no config.json.
 
Uso nos outros arquivos:
    from trifbr_config import CFG, EST, TXT, TIMING, EXP, BLOCOS
"""

import json
import os
 
# ─────────────────────────────────────────────────────────────────────────────
# Caminho do config.json — sempre na mesma pasta que este arquivo
# ─────────────────────────────────────────────────────────────────────────────
_DIR = os.path.dirname(os.path.abspath(__file__))
_CONFIG_PATH = os.path.join(_DIR, "config.json")
 
if not os.path.exists(_CONFIG_PATH):
    raise FileNotFoundError(
        f"config.json não encontrado em: {_CONFIG_PATH}\n"
        "Verifique se o arquivo está na mesma pasta que trifbr_config.py."
    )
 
with open(_CONFIG_PATH, encoding="utf-8") as _f:
    CFG = json.load(_f)

# ─────────────────────────────────────────────────────────────────────────────
# Atalhos — evita CFG["estimulos"]["video_alvo"]["tamanho"] em todo lugar
# ─────────────────────────────────────────────────────────────────────────────
CORES  = CFG["cores"]
EXP    = CFG["experimento"]
EST    = CFG["estimulos"]
TXT    = CFG["textos"]
TIMING = CFG["timing"]
TREINO = CFG["treino"]
BLOCOS = CFG["blocos"]
SAIDA  = CFG["saida"]
 
# Tamanhos e posições já como tuplas, prontas para o PsychoPy
VIDEO_SIZE = tuple(EST["video_alvo"]["tamanho"])
VIDEO_POS  = tuple(EST["video_alvo"]["posicao"])
IMAGE_SIZE = tuple(EST["imagens_resposta"]["tamanho"])
IMAGE_POS  = [tuple(p) for p in EST["imagens_resposta"]["posicoes"]]

# ─────────────────────────────────────────────────────────────────────────────
# Verificação rápida ao rodar diretamente: python trifbr_config.py
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== config.json carregado com sucesso ===\n")
    print(f"Experimento : {EXP['nome']}")
    print(f"Tela cheia  : {EXP['tela_cheia']}")
    print(f"Janela      : {EXP['tamanho_janela']}")
    print(f"\nVídeo  — tamanho: {VIDEO_SIZE}  posição: {VIDEO_POS}")
    print(f"Imagem — tamanho: {IMAGE_SIZE}")
    print(f"Posições das imagens:")
    for i, pos in enumerate(IMAGE_POS):
        print(f"  imagem {i+1}: {pos}")
    print(f"\nTiming:")
    for k, v in TIMING.items():
        print(f"  {k}: {v}")
    print(f"\nBlocos ({len(BLOCOS)} total):")
    for i, b in enumerate(BLOCOS):
        print(f"  {i+1}. {b['nome']}")
        print(f"     CSV   : {b['arquivo_csv']}")
        print(f"     Ordem : {b['ordem']}")
    print(f"\nTextos ({len(TXT)} entradas):")
    for k in TXT:
        preview = TXT[k].replace('\n', ' ')[:60]
        print(f"  {k}: \"{preview}...\"")