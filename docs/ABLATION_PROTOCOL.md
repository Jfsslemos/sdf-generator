# Protocolo executável — A0/A1/A2

Este protocolo define as comparações internas obrigatórias da dissertação. Ele só recebe artefatos da execução final rastreável; smoke, piloto e benchmark AMP não entram como resultado científico.

## Entradas esperadas após E0

No diretório final de meshing da cena `study`:
- `mesh_geometry.ply`: geometria explícita sem depender de cor para identificar instâncias;
- `mesh_instances.ply`: visualização colorida por instância;
- `instance_labels.npz`: `vertex_instance_id`, vértices e triângulos;
- `study.ply`: referência DM-SR usada pelo protocolo oficial.

## A0 — DM-NeRF raw

A0 é a geometria extraída diretamente do campo neural antes do pós-processamento proposto.

Comando geométrico:

```bash
python tools/evaluate_mesh_distance.py \
  mesh_geometry.ply study.ply \
  --samples 200000 --thresholds 0.01 0.02 0.05 \
  --out results/a0_geometry.json
```

Interpretação: Precision, Completeness, F-score e distâncias de superfície descrevem a geometria da saída neural. Deve ser declarada a limitação de que o meshing oficial usa a malha GT para definir o bounding frame.

## A1 — separação explícita de instâncias

A1 usa os IDs explícitos exportados pelo runner. Não converte RGB em identidade semântica.

```bash
python tools/postprocess_instances.py \
  instance_labels.npz results/a1_instances
```

`instances.json` registra:
- número de instâncias com faces;
- vértices/faces/área/bounds por instância;
- fração de faces cujos três vértices têm o mesmo ID;
- faces de fronteira não atribuídas silenciosamente.

A1 não deve ser comparada a A0 por PSNR/SSIM/LPIPS nem por uma distância geométrica que a separação não altera. Sua evidência é estrutural: objetos individualizados e, posteriormente, manipulação independente no Gazebo.

## Gate para o piso

A2 **não será executada até o ID do piso ter origem rastreável**. O ID não será inferido apenas por cor da malha. A fonte deverá ser registrada no resultado (metadado do DM-SR, mapeamento do experimento ou evidência equivalente).

Após identificar `FLOOR_ID`, usar o mesmo `instance_labels.npz`:

```bash
python tools/evaluate_planarity.py mesh_geometry.ply \
  --labels instance_labels.npz --instance-id FLOOR_ID \
  --out results/a1_floor.json

python tools/regularize_floor.py mesh_geometry.ply results/a2_regularized.ply \
  --labels instance_labels.npz --instance-id FLOOR_ID \
  --report results/a2_floor_regularization.json

python tools/evaluate_planarity.py results/a2_regularized.ply \
  --labels instance_labels.npz --instance-id FLOOR_ID \
  --out results/a2_floor.json
```

Métricas pareadas: média absoluta, RMSE, P95 e fração de inliers. P95 é a medida primária da ablation de piso.

## A2 — pipeline completo

A2 = A1 + regularização do piso. Depois da geração dos objetos, a cena será validada funcionalmente no Gazebo Classic por:
1. carregamento/parsing;
2. remoção/reposicionamento independente;
3. colisão/superfície de apoio;
4. navegação simples, se o teste histórico puder ser reproduzido sem implementação nova relevante.

## Não fazer

- não usar `semantic_classes.json` histórico como GT da execução atual sem provar o mapeamento;
- não tratar cores RGB como classe sem rastreabilidade;
- não somar métricas heterogêneas em uma pontuação única;
- não alterar tolerâncias depois de observar o resultado final.
