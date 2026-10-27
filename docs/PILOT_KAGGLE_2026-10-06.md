# Piloto de desempenho — Kaggle/Tesla T4 — 06/10/2026

## Artefato analisado
Bundle: `dmnerf-results-bundle(1).zip`.

## Resultado
O piloto de 2000 iterações foi concluído sem erro com a configuração oficial de treino da cena `study`:
- `N_train=3072`;
- `N_samples=64`;
- `N_importance=128`;
- 300 imagens de treino, 100 de teste;
- Torch 2.2.2+cu118 em Tesla T4;
- upstream DM-NeRF `4752087038c503cd608aa9dbd8861f3fc9259581`.

Estado final:
- iteração: 1999;
- tempo interno de treino: 3168.95 s;
- tempo do estágio: 3172.19 s;
- velocidade média estável: ~1.58 s/iteração (~0.632 it/s);
- pico de memória PyTorch: 11.90 GB;
- telemetria nvidia-smi: ~13.89 GiB usados na GPU ativa;
- utilização média da GPU ativa: ~97.3%;
- segunda Tesla T4 permaneceu ociosa.

A perda total caiu de 5.03 na iteração 0 para ~1.08 na iteração 1999. O PSNR reportado no batch de treino chegou à faixa de ~27–29 dB nas últimas centenas de iterações. Esses valores de treino não substituem avaliação no conjunto de teste.

## Custo projetado em uma T4
Usando 1.58 s/iteração:
- 200k iterações: ~87 h;
- 250k: ~109 h;
- 300k: ~131 h;
- 500k: ~219 h.

Portanto, 500k não é um alvo racional no caminho crítico gratuito.

## Alinhamento com o artigo
O artigo do DM-NeRF informa que, para os experimentos, as cenas normalmente convergem em **200–300k iterações**, com batch de 3072 raios. Também informa ~0.27 s/iteração e ~24 GB em uma RTX 3090. Assim, o alvo final foi alterado de 500001 para 200001 iterações, com possibilidade de extensão a 300001 somente se a avaliação indicar necessidade.

Essa alteração não reduz arbitrariamente o protocolo abaixo do intervalo publicado; ela usa o limite inferior do intervalo de convergência informado pelos autores.

## Decisão de engenharia antes do treino longo
Não gastar cota gratuita em sessões de ~9 h ainda. O Kaggle expõe duas T4, mas o upstream usa apenas `cuda:0`. Primeiro medir mixed precision (AMP) em 500 iterações com as mesmas amostras/rays. Se o ganho não for suficiente, implementar paralelização em duas GPUs.

## Gate
Próxima execução: `notebooks/DMNeRF_Kaggle_AMP_Benchmark.ipynb`.

Critério:
- loss finita;
- checkpoint válido;
- estimativa de s/iteração significativamente menor que 1.58;
- memória reduzida sem alteração das perdas/objetivo matemático.

Somente após esse benchmark o treino de 200k será iniciado.
