# DM-NeRF/DM-SR em GPU gratuita

## Kaggle: ação necessária do titular

1. Abra um Notebook na sua conta. Em **File → Import Notebook**, importe `notebooks/DMNeRF_Kaggle_Study.ipynb` do repositório (URL ou upload conforme a interface).
2. Ative **GPU** e **Internet** nas opções da sessão. Se Kaggle exigir verificação de conta, faça essa etapa.
3. Execute **Save Version → Save & Run All**. Nenhuma célula precisa ser editada.
4. Preserve `dmnerf-results/` e `dmnerf-results-bundle.zip` nos outputs. Envie o pacote para revisar custo/VRAM antes de ampliar o experimento.
5. Para continuar, importe `DMNeRF_Kaggle_Resume.ipynb`, anexe o output anterior via **Add Input → Notebook Output** e execute com GPU/Internet. Checkpoints antigos do runner anterior não são retomados automaticamente: não têm RNG/identidade suficientes.

No Colab Free, abra os links do README, ative GPU e autorize Drive. O diretório `MyDrive/dissertacao-dmnerf/dmnerf-results` preserva os checkpoints. I/O no Drive entra no custo medido. Não altere o diretório entre sessões.

Kaggle/Colab controlam disponibilidade e duração da GPU. Não há compra automática, promessa de cota fixa nem contorno de limites. Só GPU 0 é usada; duas T4 não são tratadas como memória unificada. Referências: https://www.kaggle.com/docs/notebooks e https://research.google.com/colaboratory/faq.html.

## Perfis

| Perfil | Treino | Avaliação/meshing | Finalidade |
|---|---|---|---|
| smoke | 3 passos, primeira imagem de treino, 64 raios | primeira vista 400×400; grade 32³ | diagnóstico, sem validade como resultado científico |
| pilot | até 2000 passos ou 1 hora; 3072 raios oficiais | notebook faz somente treino | medir viabilidade/custo |
| full | até 500001 passos acumulados, até 9 horas por processo | 100 vistas + grade 256³ somente após treino completo | candidato experimental sujeito a revisão |

Smoke usa `raw/study/smoke`; piloto/full usam `raw/study/experiment`. O segundo nunca retoma pesos do primeiro. Mantidos N_samples=64 e N_importance=128. Inferência usa N_test menor que o oficial apenas para dividir os mesmos raios em lotes.

Os limites são de processamento, não garantias da plataforma. Instalação/download adicionam tempo. Avaliação e mesh têm timeout de 15 min cada no smoke e 2 h cada nos demais perfis. O treino salva ao atingir seu orçamento; encerramento abrupto recupera só o último checkpoint persistido. Não há retomada parcial de uma imagem de avaliação; essa etapa recomeça.

OOM gera erro e log, não redução silenciosa de batch/resolução. Ajustes experimentais exigem configuração e registro próprios. Conferir custo do piloto antes de comprometer cota com 500001 passos ou mais cenas.

## Automação e rastreabilidade

- Upstream fixado por SHA, patches verificam conteúdo esperado e checkout alterado é recusado.
- ZIP oficial de 1.016.414.110 bytes verificado por SHA-256 `146ddd88d34cf8efc3357737871325f2ad1fe7584f7e20fc8ec75f5d3baed602`; somente study é extraída.
- Validam-se contagens, dimensões, rótulos, poses, paleta HDF5 e entradas do meshing. RGB/máscara/pose seguem ordenação do loader oficial; não se alega calibração independente.
- Ambiente isolado preserva o kernel hospedado. Python 3.10.16, Torch 2.2.2 e dependências diretas fixadas. Freeze resolvido é reutilizado no resume; incompatibilidade falha explicitamente.
- Checkpoints atômicos com modelos, otimizador, iteração e RNG. Seeds Python/NumPy=0; Torch/CUDA=3. Não garante identidade bit a bit entre GPUs diferentes.
- Avaliação periódica interna removida, com avaliação em etapa separada. SSIM adapta multichannel para channel_axis; np.float vira float; grade/densidade de mesh ficam em CPU. Essas diferenças estão no diff salvo e na auditoria.
- LPIPS baixa os pesos VGG oficiais na primeira avaliação; mantenha Internet ativa.

## Saídas

| Arquivo/diretório | Conteúdo |
|---|---|
| dataset_manifest.json | SHA-256 por arquivo, contagens, fonte e upstream |
| environment.freeze.txt / environment.json | ambiente realmente instalado |
| upstream.patch / *-run.json / *-official-config.txt | diff, perfil, commit e hashes do executor, GPU e config oficial |
| stages.jsonl / *.log / *-gpu.csv | comandos, tempo, exit status e telemetria bruta |
| raw/study/*/latest.tar | checkpoint nativo Torch; carregar apenas saídas próprias/confiáveis |
| training.jsonl / training_state.json | perdas, iterações, tempo e pico de alocação PyTorch |
| render_test_*/test_results.txt | PSNR, SSIM, LPIPS, AP50/75/80/85/90/95 por vista e média |
| derived/*/metrics.csv | tabela derivada, separada da fonte bruta |
| mesh_*/mesh_geometry.ply / mesh_instances.ply / instance_labels.npz | geometria e IDs preditos por vértice, quando houver superfície |
| mesh_*/study.ply / color_study.ply | exportação oficial; cores remapeadas não comprovam categoria semântica |
| mesh_status.json | ausência de superfície ou malha vazia após limpeza |
| dmnerf-results-bundle.zip | pacote de saídas; também gerado se uma etapa executada falhar |

`nvidia-smi` amostra uso global; `max_vram_bytes` mede alocação PyTorch. Não são a mesma medida. O pacote não inclui ambiente nem dataset completo. O trabalho temporário fica em /kaggle/temp ou /content; a saída fica em /kaggle/working ou Drive.

## CLI reproduzível

```bash
python tools/dmnerf/bootstrap.py --work /tmp/dmnerf-work
/tmp/dmnerf-work/env/bin/python tools/dmnerf/prepare.py --work /tmp/dmnerf-work
/tmp/dmnerf-work/env/bin/python tools/dmnerf/run.py --work /tmp/dmnerf-work --output "$PWD/results/gpu" --profile smoke
/tmp/dmnerf-work/env/bin/python tools/dmnerf/run.py --work /tmp/dmnerf-work --output "$PWD/results/gpu" --profile pilot --stages train
/tmp/dmnerf-work/env/bin/python tools/dmnerf/run.py --work /tmp/dmnerf-work --output "$PWD/results/gpu" --profile full
```

Reutilizar ZIP: `prepare.py --archive /caminho/dmsr.zip`. Validar em CPU: bootstrap com `--cpu`; run com `--profile smoke --allow-cpu`. CPU não valida compatibilidade/desempenho CUDA.

Testes:
```bash
DMNERF_UPSTREAM=/tmp/dmnerf-work/DM-NeRF /tmp/dmnerf-work/env/bin/python -m unittest discover -s tests -v
```

O teste de superfície positiva usa uma esfera sintética para verificar exportação de IDs/PLY. Isso não é reconstrução da cena study. Impacto: procedimento reproduzível para E0 e instrumentação de E3; avançar para E1/E2 somente após saídas reais adequadas e identidade do piso estabelecida.
