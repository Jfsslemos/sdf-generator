# Work status

Atualizado em 2026-10-06.

## Concluído
- branch de trabalho `dissertacao-2026` criada sem alterar `master`;
- decisões metodológicas e definition of done registradas;
- repositório legado auditado;
- código oficial do DM-NeRF auditado;
- confirmado que DM-SR/DM-NeRF usa RGB + poses + supervisão 2D de instâncias;
- confirmado que a avaliação oficial gera PSNR, SSIM, LPIPS e APs de instância;
- confirmado que o modo de meshing usa uma malha de referência do DM-SR;
- identificada dependência metodológica: essa malha de referência informa o bounding frame do meshing oficial;
- runner para GPU gratuita no Kaggle adicionado;
- notebooks Kaggle/Colab de início e continuação adicionados;
- ferramentas de avaliação geométrica, planaridade e regularização do piso adicionadas;
- pergunta/objetivos científicos corrigidos em rascunho, sem sobrescrever a dissertação;
- plano experimental reduzido ao caminho crítico;
- smoke test real executado no Kaggle/Tesla T4 em 06/10: PASS.

## Evidência do smoke de 06/10
O bundle recebido confirma a execução da stack original Python 3.7.12 + PyTorch 1.8.1+cu111 + CUDA 11.1 em Tesla T4. O DM-SR/study foi carregado, o modelo treinou três iterações, gerou checkpoints e completou a avaliação interna de 10 vistas.

Os números do smoke não têm validade experimental por se tratar de modelo praticamente não treinado. O objetivo desse passo era exclusivamente validar dataset, loader, GPU, modelo, render e avaliador. Proveniência e valores foram registrados em `SMOKE_KAGGLE_2026-10-06.md`.

A malha de referência `study_ground_truth.ply` recuperada tem 437008 vértices e 844701 faces, com extensão aproximada 7.0 × 1.8125 × 7.0 m.

## Estado do executor
O executor foi revisado sobre `8727662` e publicado no commit `02a1f7c510d644157a6d37f994288bf270e6d34b`: upstream/dataset fixados, smoke isolado do experimento, retomada com RNG/otimizador, orçamento de tempo e notebooks de continuação.

O bundle do smoke foi gerado pelo executor anterior e, por isso, seus checkpoints não serão misturados ao experimento principal. Isso não perde trabalho científico: o smoke já cumpriu seu objetivo de compatibilidade.

## Bloqueio externo atual
O bloqueio de compatibilidade com GPU gratuita foi removido. O próximo passo dependente do usuário é apenas iniciar o notebook Kaggle **atualizado** para executar o perfil piloto. O piloto mede velocidade e VRAM com os parâmetros oficiais antes de gastar cota em 500001 passos.

## Próxima sequência
1. executar perfil piloto no Kaggle (até 2000 passos / 1 h);
2. medir iterações/s, VRAM e estimar custo para 500001 passos;
3. escolher número de sessões gratuitas e iniciar treino resumível;
4. avaliação oficial;
5. meshing;
6. pós-processamento e ablation do piso;
7. métricas/tabelas;
8. integração no texto.

Veja também `GPU_RUNBOOK.md`, `RUNNER_AUDIT_2026-10-06.md` e `SMOKE_KAGGLE_2026-10-06.md`.

## Incidente de compatibilidade no runner atual — 06/10
A primeira execução do runner Torch 2.x chegou ao avaliador, produziu PSNR/SSIM/LPIPS da primeira vista e falhou no cálculo de AP por mistura CPU/CUDA no código upstream. O problema foi corrigido no patch de compatibilidade sem alterar a definição da métrica. Notebooks também foram ajustados para atualizar a branch e recriar o workspace temporário em reruns. Próxima ação do usuário: executar novamente o notebook Study atualizado; se o smoke passar, o piloto inicia automaticamente.

## Notebook Study — erro de sintaxe corrigido em 06/10
A execução mais recente chegou a preparar ambiente, GPU e dataset, mas parou antes do smoke por um erro de sintaxe introduzido na célula do comando smoke: faltava o parêntese final em `run(... '--stages','train')`. Não houve falha do DM-NeRF nem consumo de uma hora de piloto. Kaggle e Colab Study foram corrigidos; commit Kaggle Study `e03dcf5ee9839cf7f30b54e82e784450030c9149`. Também foi adicionado workflow de CI para compilar todas as células dos notebooks antes de futuras execuções GPU.
