# Baseline e ablation — plano mínimo sob prazo

## Decisão
Os baselines **não serão omitidos**, mas também não bloqueiam o treino principal. O protocolo final terá duas camadas de comparação.

### 1. Ablation interna — obrigatória
Avaliar a mesma reconstrução `study` em três estados:

- **A0 — DM-NeRF raw:** saída antes do pós-processamento;
- **A1 — DM-NeRF + separação de instâncias:** objetos explicitamente individualizados;
- **A2 — pipeline completo:** A1 + regularização geométrica do piso.

Essa comparação é a mais importante para a dissertação porque mede diretamente o efeito do que foi adicionado após o DM-NeRF.

As métricas não serão agregadas artificialmente em uma pontuação única. Cada transformação será medida apenas no que pode alterar:
- A0→A1: estrutura/individualização, número de objetos, manipulação independente, carregamento no simulador;
- A1→A2: residual planar do piso, colisões/contato/navegação e efeitos geométricos locais;
- fidelidade visual do DM-NeRF não será atribuída ao pós-processamento.

### 2. Baseline externo — P1, executar em paralelo ao treino
Candidato principal: **COLMAP + reconstrução densa/OpenMVS ou saída geométrica equivalente**, usando a mesma cena `study`.

Escopo da comparação externa: **geometria**, não decomposição semântica. Comparar a geometria reconstruída com a malha de referência DM-SR por Precision, Completeness, F-score e distância simétrica/Chamfer nas mesmas tolerâncias fixadas para o método principal.

Razões para escolher esse baseline:
- representa reconstrução multivista clássica e amplamente reconhecida;
- não exige treinar outra rede neural por dezenas de horas;
- fornece uma referência externa independente para a parte geométrica;
- evita um benchmark amplo que colocaria o prazo em risco.

Se COLMAP/OpenMVS consumir mais de um dia de engenharia para ficar operacional no DM-SR, ele será cortado e a dissertação manterá A0/A1/A2 como comparação experimental principal, complementada por comparação com resultados publicados na literatura claramente marcados como resultados de terceiros.

## Não executar agora
Não treinar Vanilla NeRF, Nerfacto, Semantic-NeRF, Panoptic Lifting ou outro campo neural adicional apenas para "ter baseline". Isso exigiria outra rodada longa de GPU e mudaria o caminho crítico.

## Paralelismo
Enquanto as sessões Kaggle do DM-NeRF rodam em background:
1. preparar e tentar o baseline geométrico externo;
2. preparar scripts finais A0/A1/A2;
3. avançar texto de metodologia/avaliação;
4. não interromper o treino principal para isso.


## Implementação preparada em 06/10/2026

Foi adicionado um baseline geométrico reproduzível com poses conhecidas:
- `tools/baselines/prepare_colmap_dmsr.py` converte as poses camera-to-world do DM-SR/NeRF para o formato world-to-camera do COLMAP e escreve `cameras.txt`, `images.txt` e `points3D.txt`;
- `tools/baselines/run_colmap_dmsr.py` executa `image_undistorter`, `patch_match_stereo` e `stereo_fusion`;
- `notebooks/DM_SR_COLMAP_Baseline.ipynb` automatiza o baseline no Kaggle e mede a saída `fused.ply` contra `study.ply`.

Como o modelo esparso usa poses conhecidas e não contém pontos 3D, as imagens fonte do PatchMatch são especificadas explicitamente e o intervalo de profundidade é fixado em 4–15, igual ao protocolo DM-NeRF da cena `study`. O notebook não deve disputar GPU com uma sessão longa do DM-NeRF; executar entre sessões.

Este baseline ainda está **preparado, não validado em CUDA**. Nenhum número dele entra no texto até a execução real e a inspeção de pose/escala.
