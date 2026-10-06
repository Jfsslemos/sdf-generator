# Benchmark AMP — Kaggle/Tesla T4 — 06/10/2026

## Resultado
O benchmark AMP de 500 iterações concluiu com sucesso na cena `study`, usando a mesma configuração de treino do piloto (`N_train=3072`, `N_samples=64`, `N_importance=128`).

Medições:
- 500 passos;
- 297.2148 s de tempo interno de treino;
- 0.59443 s/iteração;
- 1.6823 iterações/s;
- projeção de 33.02 h para 200k;
- projeção de 49.54 h para 300k;
- pico PyTorch: 5.58 GiB.

Comparação com FP32:
- piloto FP32: ~1.58 s/it;
- AMP: ~0.594 s/it;
- speedup aproximado: 2.66x;
- memória PyTorch caiu de ~11.90 GiB para ~5.58 GiB.

A trajetória inicial de otimização permaneceu saudável: loss total caiu de 5.03 na iteração 0 para 2.15 na iteração 400; PSNR de treino subiu de 4.16 para 23.24 dB nesse intervalo. Esses valores são apenas diagnóstico de treino, não métricas finais de teste.

## Decisão
AMP foi aceito como caminho de execução por reduzir drasticamente custo e memória sem sinal de instabilidade no benchmark. Não é necessário bloquear o treino de 200k aguardando paralelização em duas GPUs.

A segunda T4 continua potencialmente útil, mas multi-GPU passa a ser otimização opcional. A prioridade é iniciar imediatamente o treino resumível de 200001 passos.

## Sessões Kaggle
O orçamento de cada sessão longa foi ajustado para 39600 s (11 h), deixando aproximadamente 1 h de margem dentro do limite de sessão de 12 h para setup, checkpoint, empacotamento e encerramento.

Na velocidade medida, 200k exige ~33 h efetivas de treino, portanto aproximadamente três sessões longas mais eventual margem curta. A execução é retomada por checkpoint.

Notebook:
`notebooks/DMNeRF_Kaggle_AMP_Resume.ipynb`

## Próximo gate
Anexar como input a saída do benchmark AMP (`dmnerf-amp-results`) e executar o notebook AMP Resume. Ao final de cada sessão, preservar e reanexar o output mais recente até `complete=true`.
