# Smoke test Kaggle — 06/10/2026

## Origem
Artefato recebido: `dmnerf_study_outputs.tar.gz`.

Este resultado foi produzido pelo primeiro executor Kaggle, antes da integração do runner resumível publicada no commit `02a1f7c510d644157a6d37f994288bf270e6d34b`. Portanto, os checkpoints `000000.tar`–`000002.tar` **não devem ser usados para retomar o experimento principal**. O resultado é evidência de compatibilidade e de carregamento correto do pipeline, não resultado científico final.

## Ambiente observado
- Python 3.7.12 (conda-forge)
- PyTorch 1.8.1+cu111
- CUDA runtime 11.1
- GPU Tesla T4
- NumPy 1.21.6
- DM-NeRF upstream: `4752087038c503cd608aa9dbd8861f3fc9259581`

Esse teste confirma que a stack original do trabalho é executável em uma T4 gratuita do Kaggle.

## Dados
A cena `study` foi localizada em DM-SR e carregada corretamente. O bundle inclui `study_ground_truth.ply` com:
- 437008 vértices;
- 844701 faces;
- limites aproximados [-3.5, -0.004468, -3.5] a [3.5, 1.808029, 3.5] m;
- extensão aproximada 7.0 × 1.8125 × 7.0 m.

## Smoke
O teste reduziu deliberadamente o protocolo para diagnóstico:
- N_train=128;
- N_test=256;
- N_samples=16;
- N_importance=32;
- 3 iterações;
- checkpoint a cada passo.

A execução chegou ao treino e à avaliação interna de 10 vistas, gerou checkpoints, renders, máscaras, matching log e `test_results.txt`.

Média do passo inicial:
- PSNR: 4.253601 dB
- SSIM: 0.000846
- LPIPS: 0.456959
- AP50: 0.027244
- AP75/AP80/AP85/AP90/AP95: 0

Esses números são esperadamente ruins para um modelo praticamente não treinado e **não devem aparecer como resultado da dissertação**. Sua utilidade é apenas demonstrar que dataset, loader, modelo, GPU, render e avaliador executaram sem falha.

## Conclusão
**Smoke PASS.**

Desbloqueado:
1. medir custo real de treino com o perfil piloto;
2. decidir a estratégia de sessões gratuitas;
3. somente depois iniciar treino experimental completo.

A próxima execução deve usar o notebook/runner atual da branch `dissertacao-2026`, que separa smoke e experimento, preserva RNG/otimizador e permite retomada controlada entre sessões.
