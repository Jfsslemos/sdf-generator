# Proveniência de resultados históricos

## Regra

Resultados históricos não entram como reprodução atual sem origem rastreável. Esta página registra a origem documental encontrada e separa explicitamente resultados publicados de resultados gerados pelo experimento de 2026.

## Tabela histórica de oito cenas

Foi localizada uma fonte primária do próprio trabalho:

**Lemos, J. F. S. S. et al. — _Digital Environment Description and Reconstruction using Panoptic Segmentation_.**

A Tabela 1 desse artigo contém os oito ambientes DM-SR e os valores abaixo:

| Cena | PSNR | SSIM | LPIPS | Decomposition (%) |
|---|---:|---:|---:|---:|
| Bathroom | 45.22 | 0.991 | 0.022 | 99.20 |
| Bedroom | 47.59 | 0.994 | 0.018 | 100.00 |
| Dining Room | 38.76 | 0.987 | 0.015 | 99.49 |
| Kitchen | 48.90 | 0.989 | 0.028 | 100.00 |
| Reception | 41.92 | 0.996 | 0.011 | 99.60 |
| Living Room | 43.74 | 0.981 | 0.024 | 100.00 |
| Study Room | 39.67 | 0.995 | 0.008 | 100.00 |
| Office | 47.01 | 0.992 | 0.012 | 99.12 |
| Mean | 44.66 | 0.991 | 0.017 | 99.58 |

Fonte pública localizada em 06/10/2026:
`https://rodrigoguerra.com/wp-content/uploads/2024/06/Digital_Environment_Description_and_Reconstruction_using_Panoptic_Segmentation.pdf`, Tabela 1.

O artigo também declara que a avaliação se baseia no DM-NeRF/DM-SR e que o estudo detalhado do pipeline usa a cena **Study Room**.

## Divergência encontrada em material secundário

Há uma tabela histórica circulando no material de trabalho com pequenas divergências, entre elas:
- Dining Room LPIPS 0.019 em vez de 0.015;
- Dining Room decomposition 99.69 em vez de 99.49;
- média PSNR 44.10 em vez de 44.66;
- média decomposition 99.68 em vez de 99.58.

Enquanto a origem dessas variantes não for identificada, **não usar os valores divergentes como resultado oficial**. Para citar resultados históricos, preferir os números da publicação primária acima e identificá-los como resultados publicados anteriormente, não como reprodução de 2026.

## Execução atual de 2026

Os resultados finais da dissertação serão registrados separadamente, com:
- commit do executor;
- configuração;
- checkpoint;
- logs;
- métricas brutas;
- ambiente;
- bundle correspondente.

Smoke, piloto FP32 e benchmark AMP são evidências de infraestrutura/custo e não substituem as métricas científicas finais.
