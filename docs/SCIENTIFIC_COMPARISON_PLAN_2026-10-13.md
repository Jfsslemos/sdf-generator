# Plano de comparação científica — 13/10/2026

## Correção de rumo

A versão LaTeX atual ainda não satisfaz sozinha a exigência de comparação com a literatura. A tabela por características é contextual, mas não substitui comparação quantitativa.

O fechamento científico passa a exigir três níveis de comparação:

1. **Reprodução direta do DM-NeRF na cena study** contra os valores publicados pelos autores no mesmo DM-SR/protocolo.
2. **Comparação de decomposição** contra os baselines Mask R-CNN e Swin Transformer publicados por Wang et al. para a mesma cena study e AP0.75.
3. **Baseline externo de geometria COLMAP** executado sobre a mesma cena e avaliado pelo mesmo protocolo de distância de superfície usado para A0.

## Comparação já disponível sem nova execução

Wang et al. (ICLR 2023), Table 1, cena study:
- PSNR 41.08 dB;
- SSIM 0.987;
- LPIPS 0.026;
- AP0.75: Mask R-CNN 96.86%, Swin Transformer 97.88%, DM-NeRF 98.86%.

Reprodução auditada desta dissertação:
- PSNR 41.1100 dB;
- SSIM 0.9875;
- LPIPS 0.0260;
- AP0.75 99.11%.

Essa comparação é diretamente pertinente porque usa a mesma cena study, a mesma família de entradas e o protocolo oficial do DM-NeRF. A dissertação deve apresentar os valores publicados e os reproduzidos em tabela separada, sem alegar significância estatística com uma única cena.

## Comparação externa ainda necessária

COLMAP+dense MVS deixa de ser opcional. O notebook `notebooks/DM_SR_COLMAP_Baseline.ipynb` foi preparado para execução única no Kaggle.

O baseline será avaliado contra o mesmo `study.ply`, com:
- 200.000 amostras;
- seed 42;
- limiares 1, 2 e 5 cm;
- mesmas definições de Precision, Completeness, F-score e distâncias direcionais usadas em A0.

Além da tabela quantitativa, o `fused.ply` será renderizado em enquadramentos equivalentes aos usados para A0, fornecendo comparação qualitativa de geometria.

## Contextualização com métodos panópticos posteriores

Resultados publicados em Replica/ScanNet/HyperSim para Panoptic Neural Fields, Panoptic Lifting e Contrastive Lift podem ser apresentados em uma tabela de **contexto de literatura**, mas não misturados numericamente aos resultados DM-SR desta dissertação, pois datasets e métricas não são equivalentes.

## Figuras

As figuras atuais com rótulos rasterizados/clipped devem ser substituídas. Regra editorial:
- nenhum texto sobreposto à área de dados;
- identificadores de linhas/colunas ficam na legenda ou em subcaptions LaTeX;
- nenhuma captura cinza do Gazebo entra na versão destinada ao orientador;
- a captura do Gazebo será refeita com materiais visuais distintos por instância;
- A0/A1 devem usar renderização de superfície legível, não nuvem preta densa.

## Critério de fechamento

A dissertação não deve ser descrita como pronta enquanto:
- o baseline COLMAP não tiver sido executado ou houver bloqueio técnico documentado;
- as figuras qualitativas defeituosas não tiverem sido substituídas;
- a seção de comparação quantitativa com a literatura não estiver incorporada;
- uma captura interpretável do Gazebo não estiver disponível.
