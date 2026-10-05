# Achados técnicos confirmados — DM-NeRF / código recuperado

## Entrada real do DM-NeRF no DM-SR
O loader oficial datasets/loader_dmsr.py não usa apenas RGB e poses. O treinamento também carrega mapas 2D de instância em train/semantic_instance e test/semantic_instance, além de ins_rgb.hdf5. Portanto, a dissertação não deve afirmar que a versão atual aprende a decomposição somente a partir de RGB posicionadas.

Como OneFormer saiu do caminho crítico, a contribuição deve ser enquadrada na transformação de uma reconstrução neural já supervisionada por instâncias 2D em uma cena estruturada para simulação, somada à avaliação da cadeia.

## Ground truth geométrico
O test_dmsr.py oficial procura data/dmsr/<scene>/<scene>.ply no modo mesh. Assim, o protocolo do DM-SR espera uma malha de referência por cena, o que permite avaliar geometria com Precision, Completeness, F-score e Chamfer.

## Limitação importante do meshing oficial
tools/mesh_generator.py usa trimesh.bounds.oriented_bounds sobre a malha de referência da cena para definir a transformação/volume da grade consultada pelo campo neural. Portanto, uma avaliação geométrica contra essa mesma referência não é totalmente cega: o GT informa o bounding frame da extração. Isso deve ser declarado como limitação ou substituído por um volume independente se houver tempo.

## Métricas oficiais de decomposição
O evaluator oficial calcula AP em IoU 0.50, 0.75, 0.80, 0.85, 0.90 e 0.95. O test_results.txt contém PSNR, SSIM, LPIPS e esses APs por vista, além da média. A dissertação deve rastrear a origem da porcentagem de decomposição histórica e preferir a nomenclatura exata do código/paper.

## Código recuperado do TCC
O sdf-generator original contém pós-processamento e integração Gazebo, não o DM-NeRF completo. Há paths absolutos, escala padrão zero no sdf_writer.py e erros em multi_sdf_writer.py. Os scripts legados devem ficar preservados como histórico; novas ferramentas portáveis ficam em tools/.
