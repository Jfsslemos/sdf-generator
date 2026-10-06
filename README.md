# sdf-generator — dissertação 2026

Método mantido: DM-NeRF/DM-SR com RGB, poses e supervisão 2D de instâncias, seguido de pós-processamento e Gazebo Classic. Leia [AGENTS.md](AGENTS.md) e [docs/DECISIONS.md](docs/DECISIONS.md).

## Executar sem programar

- **Kaggle, prioridade:** importe [DMNeRF_Kaggle_Study.ipynb](notebooks/DMNeRF_Kaggle_Study.ipynb), ative GPU e Internet, execute **Save Version → Save & Run All**. Ele instala tudo, baixa/valida os dados e executa smoke test + piloto de até uma hora.
- **Continuar no Kaggle:** importe [DMNeRF_Kaggle_Resume.ipynb](notebooks/DMNeRF_Kaggle_Resume.ipynb) e anexe a saída anterior em **Add Input → Notebook Output**. Execute todas as células com GPU/Internet.
- **Colab Free:** [abrir início](https://colab.research.google.com/github/Jfsslemos/sdf-generator/blob/dissertacao-2026/notebooks/DMNeRF_Colab_Study.ipynb) ou [abrir continuação](https://colab.research.google.com/github/Jfsslemos/sdf-generator/blob/dissertacao-2026/notebooks/DMNeRF_Colab_Resume.ipynb). Ative GPU e autorize Drive.

Não é necessário editar `RUN_FULL`, caminhos ou comandos. O primeiro uso executa somente `study`; smoke e experimento têm checkpoints separados. Disponibilidade e cota gratuitas dependem da conta. Não se promete convergência em uma sessão.

Procedimentos e limitações: [GPU_RUNBOOK.md](docs/GPU_RUNBOOK.md). Estado revisado: [RUNNER_AUDIT_2026-10-06.md](docs/RUNNER_AUDIT_2026-10-06.md).
