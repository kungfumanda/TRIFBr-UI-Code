# TRIFBr — Próximos passos

## Status atual
O experimento está rodando com a arquitetura configuration-driven completa:
- `config.json` — parâmetros, textos, blocos
- `trifbr_config.py` — carrega o JSON
- `trifbr_routines.py` — todas as rotinas do experimento
- `trifbr.py` — flow principal
- `trifbr_ui.py` — interface gráfica de configuração e lançamento

---

## Pendente para amanhã

### 1. Testar o novo CSV de saída
A última alteração substituiu o `ExperimentHandler` do PsychoPy por um
`csv.DictWriter` manual. Ainda não foi testado. Verificar:
- O arquivo é gerado na pasta `data/` com o nome correto
- As 13 colunas aparecem corretamente
- As notas da sessão aparecem em todas as linhas
- Nenhum arquivo extra do PsychoPy é gerado junto

### 2. Tela de introdução na UI (trifbr_ui.py)
Adicionar uma aba ou tela inicial na interface com:
- Nome do experimento
- Versão
- Instruções rápidas de uso para o experimentador
- (Discutir o conteúdo exato)

### 3. Testar com todos os blocos ativos
Até agora só o bloco 1 foi testado. Quando os CSVs dos outros blocos
estiverem prontos, testar o fluxo completo com os 5 blocos.

### 4. Verificar comportamento do Escape
O Escape fecha o experimento no meio de qualquer rotina, mas o CSV
não é salvo nesse caso. Decidir se quer salvar os dados parciais
quando o experimento é interrompido.

### 5. Voltar pythonw.exe na UI
Durante os testes foi trocado para `python.exe` para ver erros.
Quando estiver estável, voltar para `pythonw.exe` para não mostrar
terminal na coleta real:
```python
PSYCHOPY_EXE = r"C:\Program Files\PsychoPy\pythonw.exe"
```

### 6. Validação clínica (longo prazo)
Conforme descrito no TCC (Seção 7.1), a próxima etapa científica é
a validação psicométrica com pacientes e controles saudáveis usando
a infraestrutura construída aqui.

---

## Estrutura de pastas atual
```
projeto/
├── trifbr_ui.py
├── conditions/
│   ├── conditions-BT.csv
│   ├── conditions-B1.csv
│   └── ...
├── stimuli/
│   ├── BT/
│   ├── B1/
│   └── ...
└── logic/
    ├── trifbr.py
    ├── trifbr_config.py
    ├── trifbr_routines.py
    ├── config.json
    └── data/
        └── TRIFBr_participant_[ID]_[data].csv
```

---

## Arquivos que mudaram na última sessão
- `trifbr.py` — removido ExperimentHandler, adicionado csv.DictWriter e notas da sessão
- `trifbr_routines.py` — routine_trial agora recebe exp_info e resultados em vez de this_exp
- `trifbr_ui.py` — caminhos ajustados para estrutura com pasta logic/