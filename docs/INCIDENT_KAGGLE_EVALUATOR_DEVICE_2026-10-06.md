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


## Diagnóstico fechado com o bundle da versão 2

O bundle `dmnerf-results-bundle.zip` contém o traceback completo da segunda tentativa. A primeira correção moveu `IoUs_Metrics`, `confidence` e `tp_list` para CPU, mas o upstream chama `torch.set_default_tensor_type('torch.cuda.FloatTensor')` quando CUDA está disponível. Assim, `torch.arange(len(tp_list))` continuava sendo criado em CUDA mesmo com `tp_list` em CPU.

Erro observado:

```
RuntimeError: Expected all tensors to be on the same device, but found at least two devices, cuda:0 and cpu!
```

A correção final torna explícito o device de **todos** os tensores auxiliares do cálculo de AP:
- `torch.arange(..., device=tp_list.device)`;
- tensores de borda de `mrec` e `mprec` criados no mesmo device/dtype de `rec`/`prec`;
- `torch.arange` do método de 11 pontos no device de `rec`.

Commit da correção final: `17db88cad7fb9fcec3b194c7ebaa9100e97eaea4`.

O bundle também confirma que o treino do smoke completou 3/3 iterações em 12,05 s de estágio total, com pico PyTorch ~296,6 MB no último passo. Esse tempo inclui inicialização e não deve ser extrapolado para o treino completo; o perfil piloto continua necessário.
