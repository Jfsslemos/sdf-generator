# Auditoria do baseline COLMAP — 13/10/2026

## Execução recebida

O bundle final do COLMAP foi auditado a partir da execução `COLMAP-KAGGLE-R7-2026-10-13`.

A execução terminou com sucesso:
- 300 vistas de treinamento;
- 10 vistas-fonte por referência;
- `PatchMatchStereo.geom_consistency=1`;
- profundidade entre 4 e 15 m;
- `StereoFusion.min_num_pixels=1`;
- PatchMatch: 1145,02 s;
- fusão: 28,97 s;
- nuvem final: 5.800.316 pontos.

## Correção necessária antes da comparação

Os números escritos diretamente pelo notebook em `geometry_metrics.json` não devem ser usados na dissertação.

Há duas diferenças de protocolo que tornavam essa avaliação direta não comparável a A0:

1. **Sistema de coordenadas.** O COLMAP reconstrói no sistema das poses DM-SR. O `mesh_generator.py` upstream do DM-NeRF consulta a rede após a transformação `network=[scene_x,-scene_z,scene_y]`, mas exporta a malha no sistema de cena. Logo a nuvem COLMAP deve ser trazida de volta por `scene=[colmap_x,colmap_z,-colmap_y]`.
2. **Suporte e cardinalidade.** O meshing oficial do DM-NeRF é limitado por uma caixa orientada definida a partir da cena de referência, com extensões fixas `[1.9,7.0,7.0]` m. A avaliação inicial deixou o COLMAP sem esse limite e ainda usou seus 5,8 milhões de pontos, enquanto A0 foi avaliada com 200.000 amostras de superfície.

A auditoria passa a usar o mesmo suporte orientado e 200.000 pontos por conjunto, semente 42. Dos 5.800.316 pontos COLMAP, 3.416.962 (58,91%) estão dentro do suporte comum.

## Resultados comparáveis

| Medida | DM-NeRF A0 | COLMAP |
|---|---:|---:|
| média predição -> referência | 0,043353 m | 0,204181 m |
| média referência -> predição | 0,041389 m | 0,081287 m |
| L1 simétrica | 0,084742 m | 0,285467 m |
| RMSE predição -> referência | 0,057569 m | 0,300792 m |
| RMSE referência -> predição | 0,049398 m | 0,139421 m |
| F-score @ 1 cm | 0,048041 | 0,028528 |
| F-score @ 2 cm | 0,196028 | 0,128814 |
| F-score @ 5 cm | 0,774982 | 0,372096 |

A 5 cm:
- A0: Precision 0,7963; Completeness 0,7548;
- COLMAP: Precision 0,2710; Completeness 0,5936.

## Interpretação

A0 apresenta F-score maior nos três limiares e menores distâncias direcionais. O COLMAP recupera pontos próximos a uma fração relevante da referência, mas com dispersão e espessamento maiores, refletidos principalmente pela Precision menor.

Esse resultado **não** é usado para alegar superioridade geral do DM-NeRF sobre COLMAP. É uma comparação externa na cena `study` sob uma configuração fixa. As poses foram fornecidas, não houve busca de hiperparâmetros e `StereoFusion.min_num_pixels=1` prioriza recuperação, podendo aumentar pontos espúrios.

## Artefatos reproduzíveis

- script: `tools/baselines/audit_colmap_common_support.py`;
- métricas: `docs/exports/colmap_common_support_metrics.json`;
- o `fused.ply` completo permanece fora do Git por tamanho.
