# Incidente Kaggle — avaliação do smoke em Torch 2.x — 06/10/2026

## Sintoma
A execução chegou corretamente ao render de avaliação e produziu PSNR/SSIM/LPIPS para a primeira vista, mas falhou em `networks/evaluator.py::calculate_ap`:

```
RuntimeError: indices should be either on cpu or on the same device as the indexed tensor (cpu)
```

## Causa
O código upstream define um `device` global como CUDA quando a GPU está disponível. A avaliação de instâncias, entretanto, move `pred_ins`/IoU/confidence para CPU. Em Torch 2.x, o caminho usado na ordenação/cálculo de AP expôs a mistura de dispositivos que não apareceu na stack histórica Torch 1.8.1.

Isso é uma incompatibilidade de execução do avaliador, não uma falha do treinamento nem um resultado científico.

## Correção
O patch de compatibilidade agora mantém explicitamente o cálculo de AP em CPU:
- `IoUs_Metrics.detach().cpu()`;
- `confidence.detach().cpu()`;
- `tp_list.cpu()`.

A operação é pequena e não altera a definição matemática de AP; apenas torna explícito o dispositivo onde o bookkeeping é feito.

Também foram atualizados os notebooks para:
- buscar a versão mais recente de `dissertacao-2026` quando reutilizados;
- recriar o workspace temporário para não misturar um checkout upstream já patchado com um patcher novo;
- limpar resultados de uma execução Study falha antes de começar um novo smoke/piloto.

## Evidência observada antes da falha
Primeira vista do smoke:
- PSNR 13.3788989662;
- SSIM 0.7588663697;
- LPIPS 0.3143649697.

Esses valores continuam sendo apenas diagnóstico de smoke e não entram nos resultados finais.

## Próximo passo
Executar novamente a versão atual de `notebooks/DMNeRF_Kaggle_Study.ipynb`. O notebook deve completar smoke e, se o smoke passar, iniciar automaticamente o piloto de até 2000 passos/1 h.
