# Sessão longa AMP 1 — Kaggle/Tesla T4 — 06–07/10/2026

## Artefato
Bundle recebido: `dmnerf-results-bundle(2).zip`.

## Identidade
- cena: `study`;
- perfil: `full`;
- alvo: 200001 iterações;
- `N_train=3072`, `N_test=1024`, `testskip=1`;
- upstream DM-NeRF: `4752087038c503cd608aa9dbd8861f3fc9259581`;
- executor: `e8bef9b7dc7732719c9ded4f0e1024db242c8baa`;
- Torch 2.2.2+cu118, Python 3.10.16;
- AMP habilitado.

## Resultado da sessão
- estágio de treino: **ok**, return code 0;
- orçamento consumido: 39603.40 s no estágio (~11 h);
- última iteração: **71121**;
- updates efetivos: **71091**;
- updates pulados pelo GradScaler: **31**;
- taxa de skip: ~0.0436%;
- `complete=false`;
- `stopped_for_budget=true`;
- iterações de loop restantes: **128879**;
- loss do estado final: **0.2338693**;
- pico PyTorch: **5.5787 GiB**.

A taxa de skip é pequena e os skips permaneceram esparsos; o último observado ocorreu na iteração 69712. Não há evidência de instabilidade numérica que justifique interromper o protocolo. O número de skips deve continuar sendo reportado e auditado nas próximas sessões.

## Throughput sustentado
A partir da iteração 1000, o tempo médio medido foi ~**0.5565 s/it** (~1.797 it/s), ligeiramente melhor que o benchmark curto de 0.594 s/it.

Na telemetria de 5 s:
- GPU 0: ~7414 MiB de memória global média, 7417 MiB máxima, ~92.7% de utilização média;
- GPU 1: 3 MiB, 0% de utilização.

A execução continua single-GPU; a segunda T4 ficou ociosa.

## Tendência de treino
As métricas impressas são de batches de treino, não de teste. Exemplos rastreáveis:
- iter 0: PSNR 4.16, total loss 5.034;
- iter 10000: PSNR 31.71, total loss 0.340;
- iter 50000: PSNR 38.84, total loss 0.331;
- iter 71100: PSNR 40.16, total loss 0.270.

Há variação batch-a-batch esperada. O diagnóstico global é de queda de loss e aumento de PSNR de treino, sem NaN/OOM/falha.

## Decisão
**Continuar o mesmo checkpoint/protocolo.** Na velocidade sustentada, restam ~19.9 h de treino, portanto duas sessões adicionais devem bastar.

Para reduzir risco de exceder a janela de 12 h na sessão que atingir 200001, o notebook Resume passa a executar **somente treino**. Avaliação oficial e meshing ficam em `DMNeRF_Kaggle_AMP_Finalize.ipynb`, em sessão separada após `complete=true`.
