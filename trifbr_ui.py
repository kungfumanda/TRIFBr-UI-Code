#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
trifbr_ui.py
------------
Interface gráfica para configurar e rodar o experimento TRIFBr.
Execute com o Python do sistema (não precisa do PsychoPy):
    python trifbr_ui.py

O PsychoPy standalone é chamado automaticamente ao clicar em Rodar.
"""

import json
import os
import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

# ─────────────────────────────────────────────────────────────────────────────
# Caminhos
# ─────────────────────────────────────────────────────────────────────────────
_DIR        = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(_DIR, "logic", "config.json")
LOGIC_DIR = os.path.join(_DIR, "logic")
TRIFBR_PATH = os.path.join(_DIR, "logic", "trifbr.py")
PSYCHOPY_EXE = r"C:\Program Files\PsychoPy\python.exe"


# ─────────────────────────────────────────────────────────────────────────────
# Helpers JSON
# ─────────────────────────────────────────────────────────────────────────────
def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# Verificação de estímulos
# ─────────────────────────────────────────────────────────────────────────────
def verificar_estimulos(cfg):
    """
    Verifica se todos os arquivos referenciados nos CSVs existem.
    Retorna (ok: bool, mensagem: str).
    """
    import csv

    erros = []
    blocos_ativos = [b for b in cfg["blocos"] if b.get("ativo", True)]
    blocos_verificar = blocos_ativos + [cfg["treino"]]

    for bloco in blocos_verificar:
        csv_path = os.path.normpath(os.path.join(_DIR, "conditions", bloco["arquivo_csv"]))
        if not os.path.exists(csv_path):
            erros.append(f"CSV não encontrado: {csv_path}")
            continue

        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, start=2):
                # Verifica vídeo
                video = os.path.normpath(os.path.join(LOGIC_DIR, row.get("Target_Video", "")))
                if not os.path.exists(video):
                    erros.append(f"Linha {i} — vídeo não encontrado: {video}")
                # Verifica imagens
                for col in ["Image_1", "Image_2", "Image_3", "Image_4"]:
                    img = os.path.normpath(os.path.join(LOGIC_DIR, row.get(col, "")))
                    if not os.path.exists(img):
                        erros.append(f"Linha {i} — imagem não encontrada: {img}")

    if erros:
        return False, "\n".join(erros)
    return True, "Todos os arquivos encontrados."


# ─────────────────────────────────────────────────────────────────────────────
# Janela principal
# ─────────────────────────────────────────────────────────────────────────────
class TRIFBrUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TRIFBr — Configuração do Experimento")
        self.root.resizable(False, False)
        self.cfg = load_config()
        self._build()

    def _build(self):
        pad = {"padx": 12, "pady": 6}

        # ── Notebook com abas ──
        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=10, pady=10)

        self._tab_blocos(nb, pad)
        self._tab_textos(nb, pad)
        self._tab_verificar(nb, pad)

        # ── Botão rodar ──
        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(fill="x", padx=10, pady=(0, 10))

        tk.Button(
            frame_bottom, text="▶  Rodar experimento",
            command=self._rodar,
            bg="#2e7d32", fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat", padx=16, pady=8, cursor="hand2",
        ).pack(side="right")

        tk.Button(
            frame_bottom, text="Salvar config.json",
            command=self._salvar,
            font=("Segoe UI", 10),
            relief="flat", padx=12, pady=8, cursor="hand2",
        ).pack(side="right", padx=(0, 8))

    # ── Aba: Blocos ──────────────────────────────────────────────────────────
    def _tab_blocos(self, nb, pad):
        frame = tk.Frame(nb)
        nb.add(frame, text="  Blocos  ")

        tk.Label(
            frame,
            text="Ative ou desative blocos para esta sessão.",
            font=("Segoe UI", 10), fg="#555",
        ).pack(anchor="w", **pad)

        self._bloco_vars = []
        for bloco in self.cfg["blocos"]:
            var = tk.BooleanVar(value=bloco.get("ativo", True))
            self._bloco_vars.append(var)
            tk.Checkbutton(
                frame, text=bloco["nome"],
                variable=var,
                font=("Segoe UI", 10),
                anchor="w",
            ).pack(fill="x", padx=16, pady=2)

    # ── Aba: Textos ──────────────────────────────────────────────────────────
    def _tab_textos(self, nb, pad):
        frame = tk.Frame(nb)
        nb.add(frame, text="  Textos  ")

        tk.Label(
            frame,
            text="Edite os textos exibidos para o participante.",
            font=("Segoe UI", 10), fg="#555",
        ).pack(anchor="w", **pad)

        # Labels amigáveis para cada chave
        labels = {
            "welcome_titulo":   "Título de boas-vindas",
            "welcome_corpo":    "Corpo de boas-vindas",
            "welcome_avanco":   "Instrução de avanço",
            "exemplo_titulo":   "Título do exemplo",
            "exemplo_continuar":"Instrução do exemplo",
            "bloco_continuar":  "Instrução entre blocos",
            "encerramento":     "Texto de encerramento",
        }

        canvas = tk.Canvas(frame, borderwidth=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas)

        inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=6)
        scrollbar.pack(side="right", fill="y", pady=6)

        self._texto_widgets = {}
        for chave, label in labels.items():
            tk.Label(inner, text=label, font=("Segoe UI", 9, "bold")).pack(
                anchor="w", pady=(8, 0))
            txt = scrolledtext.ScrolledText(
                inner, height=3, width=60,
                font=("Segoe UI", 9), wrap="word",
            )
            txt.insert("1.0", self.cfg["textos"].get(chave, ""))
            txt.pack(fill="x", pady=(2, 0))
            self._texto_widgets[chave] = txt

    # ── Aba: Verificar ───────────────────────────────────────────────────────
    def _tab_verificar(self, nb, pad):
        frame = tk.Frame(nb)
        nb.add(frame, text="  Verificar estímulos  ")

        tk.Label(
            frame,
            text="Verifica se todos os arquivos de vídeo e imagem existem.",
            font=("Segoe UI", 10), fg="#555",
        ).pack(anchor="w", **pad)

        tk.Button(
            frame, text="Verificar agora",
            command=self._verificar,
            font=("Segoe UI", 10),
            relief="flat", padx=12, pady=6, cursor="hand2",
        ).pack(anchor="w", padx=16)

        self._resultado_texto = scrolledtext.ScrolledText(
            frame, height=16, width=70,
            font=("Courier New", 9), state="disabled",
            wrap="none",
        )
        self._resultado_texto.pack(fill="both", expand=True, padx=12, pady=8)

    # ── Ações ────────────────────────────────────────────────────────────────
    def _coletar_edicoes(self):
        """Atualiza o cfg com os valores atuais da UI antes de salvar/rodar."""
        # Blocos
        for i, var in enumerate(self._bloco_vars):
            self.cfg["blocos"][i]["ativo"] = var.get()
        # Textos
        for chave, widget in self._texto_widgets.items():
            self.cfg["textos"][chave] = widget.get("1.0", "end-1c")

    def _salvar(self):
        self._coletar_edicoes()
        save_config(self.cfg)
        messagebox.showinfo("Salvo", "config.json atualizado com sucesso.")

    def _verificar(self):
        self._coletar_edicoes()
        ok, msg = verificar_estimulos(self.cfg)
        self._resultado_texto.config(state="normal")
        self._resultado_texto.delete("1.0", "end")
        self._resultado_texto.insert("1.0", msg)
        self._resultado_texto.config(state="disabled")
        if ok:
            messagebox.showinfo("Verificação", "Todos os arquivos encontrados!")
        else:
            messagebox.showwarning("Arquivos faltando", "Alguns arquivos não foram encontrados.\nVeja a lista na aba Verificar.")

    def _rodar(self):
        # Salva antes de rodar
        self._coletar_edicoes()
        save_config(self.cfg)

        # Verifica estímulos
        ok, msg = verificar_estimulos(self.cfg)
        if not ok:
            if not messagebox.askyesno(
                "Arquivos faltando",
                "Alguns arquivos de estímulo não foram encontrados.\n\n"
                "Deseja rodar o experimento mesmo assim?",
            ):
                return

        # Confirmação final
        blocos_ativos = [
            b["nome"] for b in self.cfg["blocos"] if b.get("ativo", True)
        ]
        resumo = "\n".join(f"  • {n}" for n in blocos_ativos)
        if not messagebox.askyesno(
            "Confirmar início",
            f"Blocos que serão rodados:\n{resumo}\n\nIniciar o experimento?",
        ):
            return

        # Lança o PsychoPy
        if not os.path.exists(PSYCHOPY_EXE):
            messagebox.showerror(
                "PsychoPy não encontrado",
                f"Executável não encontrado em:\n{PSYCHOPY_EXE}\n\n"
                "Verifique o caminho no arquivo trifbr_ui.py.",
            )
            return

        subprocess.Popen([PSYCHOPY_EXE, TRIFBR_PATH])
        self.root.destroy()


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = TRIFBrUI(root)
    root.mainloop()