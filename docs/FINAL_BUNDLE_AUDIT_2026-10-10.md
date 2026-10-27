# Auditoria do bundle final DM-NeRF/DM-SR — 10/10/2026

Bundle auditado: `dmnerf-results-bundle.zip`

- tamanho: 96.944.497 bytes (92,45 MiB);
- SHA-256: `196c4b5c456b589ddf124e4c70ac1caa840c9172c13348de43531d96eb064e9b`;
- integridade ZIP: aprovada; nenhum membro corrompido detectado.

## Identidade e proveniência

O experimento final declara:

- executor da dissertação: `e8bef9b7dc7732719c9ded4f0e1024db242c8baa`;
- upstream DM-NeRF: `4752087038c503cd608aa9dbd8861f3fc9259581`;
- Python 3.10.16;
- Torch 2.2.2+cu118;
- GPU: Tesla T4;
- CUDA 11.8;
- AMP habilitado no treinamento.

Os hashes internos foram rechecados contra os próprios artefatos do bundle:

- `upstream.patch`: `0cf12aad56f53400e0aac54ee76102dcc8c6bdfced6a24fa6f481b8df031a1a7` — coincide com `identity.json`;
- `dataset_manifest.json`: `38c912b6615caa5c3a549190e8567d7452f9cd97ad3077037e6b3b9518229ae0` — coincide com `identity.json`;
- `environment.freeze.txt`: `8f6a264a1444cca3a0168c49c3ff6d7808abf5e85c55184061ee065de0814083` — coincide com `identity.json`.

## Treinamento

`training.jsonl` contém 200.001 registros contínuos, de 0 a 200.000, sem gaps e sem iterações duplicadas.

Estado final:

- iteração: 200.000;
- target: 200.001;
- `complete=true`;
- `stopped_for_budget=false`;
- atualizações efetivas: 199.916;
- atualizações puladas por AMP: 85;
- perda final de treinamento: 0,1924343556;
- pico de alocação PyTorch: 5.990.076.416 bytes (~5,58 GiB).

O checkpoint `latest.tar` foi carregado estruturalmente e contém:

- pesos coarse e fine;
- estado do otimizador;
- estado do AMP scaler;
- contadores de updates efetivos e pulados;
- estados RNG de Python, NumPy, Torch e CUDA;
- iteração 200.000.

Tempos registrados das três sessões de treino:

- 39.603,400 s;
- 39.602,765 s;
- 32.260,784 s;
- total: 111.466,949 s (~30 h 57 min 47 s).

A telemetria NVIDIA registrou pico de 7.417 MiB durante as sessões de treinamento. Esse valor mede memória global reportada por `nvidia-smi` e não é equivalente ao pico de alocação PyTorch.

## Avaliação oficial

O estágio `evaluate` terminou com `status=ok`, `returncode=0`, em 2.568,477 s.

Foram verificados 100 resultados por vista, mais a linha média. O arquivo derivado `derived/experiment/metrics.csv` coincide numericamente com `render_test_200000/test_results.txt`; a recomputação das médias dos 100 frames difere apenas por arredondamento submicrométrico da serialização.

Médias oficiais:

| Métrica | Valor |
|---|---:|
| PSNR | 41,110037 |
| SSIM | 0,987517 |
| LPIPS | 0,026037 |
| AP50 | 0,995565 |
| AP75 | 0,991100 |
| AP80 | 0,984890 |
| AP85 | 0,976949 |
| AP90 | 0,931109 |
| AP95 | 0,719241 |

O diretório de render contém 100 renders RGB previstos, 100 mapas de instância previstos, 100 mapas de instância GT e 100 máscaras GT. As 400 imagens foram abertas e verificadas; todas têm resolução 400×400 e não apresentaram erro de decodificação.

## Meshing

O estágio `mesh` terminou com `status=ok`, `returncode=0`, em 109,132 s. Não há `mesh_status.json` de falha.

Artefatos explícitos principais:

- `mesh_geometry.ply`;
- `mesh_instances.ply`;
- `instance_labels.npz`.

O contrato de `instance_labels.npz` foi verificado:

- 356.272 vértices;
- 710.928 triângulos;
- IDs por vértice no intervalo 0–12;
- 13 IDs presentes;
- todos os vértices são finitos;
- todos os índices de triângulos estão dentro do intervalo;
- geometria delimitada aproximadamente por 7,0 × 1,895 × 7,0 unidades.

Na classificação de faces pela igualdade dos três IDs de vértice:

- faces homogêneas: 681.383;
- faces de fronteira: 29.545;
- cobertura conservadora por faces homogêneas: 0,9584416425 (~95,84%).

Foram identificadas 10 faces com área numérica nula ou praticamente nula entre 710.928 faces. A fração é desprezível para o contrato estrutural atual, mas deve ser preservada como observação de qualidade geométrica e não ocultada.

## Custo do Finalize

- avaliação: 2.568,477 s;
- meshing: 109,132 s;
- soma das etapas científicas do Finalize: 2.677,610 s (~44 min 38 s).

O notebook completo encerrou em aproximadamente 2.825 s incluindo preparação/empacotamento.

## Observação crítica sobre `study.ply`

O arquivo `raw/study/experiment/mesh_200000/study.ply` contido no bundle **não é a malha ground truth do DM-SR**. Pelo código oficial de `tools/mesh_generator.py`, esse arquivo é a malha reconstruída pelo marching cubes antes da limpeza, exportada com `args.expname + '.ply'`.

A referência geométrica oficial da cena deve ser obtida do dataset DM-SR validado, em `data/dmsr/study/study.ply`, cuja identidade no manifesto é:

- 437.008 vértices;
- 844.701 faces;
- 16.225.413 bytes;
- SHA-256 `8de1c71689452af874d661b610873a036fddf979b89c86704e5537561c1452fc`.

Portanto, a avaliação geométrica A0 **não deve** comparar `mesh_geometry.ply` com o `study.ply` do diretório `mesh_200000`. O protocolo de ablação foi corrigido para exigir explicitamente a referência do dataset oficial.

## Conclusão da auditoria

O bundle é **apto para uso como fonte primária dos resultados do componente neural e da malha A0**.

A auditoria não demonstra ainda:

- métricas geométricas A0 contra a malha de referência;
- separação efetivamente exportada como A1;
- identificação do piso;
- regularização A2;
- validações G0–G4 no Gazebo;
- execução do baseline COLMAP.

Esses itens devem permanecer separados e ser produzidos a partir deste bundle sem repetir treinamento ou Finalize.
