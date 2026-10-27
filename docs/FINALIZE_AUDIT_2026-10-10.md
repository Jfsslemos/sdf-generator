# Auditoria do Finalize DM-NeRF — 10/10/2026

## Fonte auditada

Bundle recebido após o notebook Finalize:

- arquivo: `dmnerf-results-bundle.zip`
- tamanho: 96.944.497 bytes
- SHA-256: `196c4b5c456b589ddf124e4c70ac1caa840c9172c13348de43531d96eb064e9b`
- teste CRC do ZIP: aprovado
- entradas no ZIP: 438

A auditoria abaixo usa somente artefatos contidos nesse bundle, salvo onde uma dependência externa é indicada explicitamente.

## Estado do treinamento

`raw/study/experiment/training_state.json`:

- iteration: 200000
- target_steps: 200001
- effective_updates: 199916
- skipped_updates: 85
- complete: true
- stopped_for_budget: false
- max_vram_bytes: 5990076416

`training.jsonl` contém 200001 registros, com iterações contínuas de 0 a 200000. Para todos os registros auditados, `effective_updates + skipped_updates = iteration + 1`.

O checkpoint `latest.tar` carrega com iteration=200000 e contém os estados das redes coarse/fine, otimizador, AMP scaler e RNG, além dos contadores de updates efetivos e pulados.

## Finalize

`stages.jsonl` registra:

- evaluate: status=ok, returncode=0, elapsed_seconds=2568.477145273;
- mesh: status=ok, returncode=0, elapsed_seconds=109.132422957.

A avaliação possui 100 vistas de teste mais a linha média. A média recomputada das 100 linhas coincide com `derived/experiment/metrics.csv`:

| PSNR | SSIM | LPIPS | AP50 | AP75 | AP80 | AP85 | AP90 | AP95 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 41.110037 | 0.987517 | 0.026037 | 0.995565 | 0.991100 | 0.984890 | 0.976949 | 0.931109 | 0.719241 |

O diretório de render contém 100 renders RGB, 100 predições de instância, 100 imagens de instância GT e 100 máscaras GT.

## Contrato da malha

Artefatos finais:

- `mesh_geometry.ply`: 356272 vértices, 710928 faces, SHA-256 `c4915fec9d1de0e3bba9fe60ee5f95782667282a83115798957d08787ed757d0`;
- `mesh_instances.ply`: 356272 vértices, 710928 faces, SHA-256 `91bce66afa30683af14515d2813d058ef58725d82b038d3718b9bdd260dda160`;
- `instance_labels.npz`: SHA-256 `7349ca0d5c11ff44c16329fd0e337fae9fdd29abad6fa60aaeb9d6568c15076d`.

`instance_labels.npz` contém 356272 vértices, 710928 triângulos e um ID inteiro por vértice. Os triângulos e coordenadas coincidem exatamente com `mesh_geometry.ply`; todos os índices são válidos; os IDs presentes são 0–12.

## A1 — separação estrutural

Aplicando a regra congelada de faces homogêneas aos IDs explícitos:

- instâncias com faces: 13;
- faces fonte: 710928;
- faces homogêneas/exportáveis: 681383;
- faces de fronteira: 29545;
- cobertura de faces: 0.9584416425 (95,8442%).

A1 não altera, por definição, a geometria das faces preservadas; esses números caracterizam a individualização estrutural e a perda explícita nas fronteiras.

## Gate do piso

A regra v2 congelada em `FLOOR_IDENTIFICATION.md`, com +Y vertical e sem uso de semântica, retorna:

- status: `selected`;
- evidence_type: `geometric_heuristic`;
- semantic_ground_truth: false;
- instance_id: 10;
- área homogênea do candidato: 45.435672 m²;
- fração horizontal: 0.879223;
- RMSE do critério geométrico de seleção: 0.020377 m.

Somente o ID 10 passou todos os gates predefinidos. O resultado deve continuar sendo descrito como candidato geométrico, não como ground truth semântico de piso.

## A1 × A2 — planaridade do candidato

Avaliação RANSAC sobre os mesmos 102064 vértices do ID 10:

| Condição | Média abs. | RMSE | P95 | Fração de inliers |
|---|---:|---:|---:|---:|
| A1, antes | 0.0205128 m | 0.0572216 m | 0.0679989 m | 0.771104 |
| A2, depois | ~6.97e-10 m | ~8.55e-10 m | ~1.68e-9 m | 1.000000 |

A projeção torna o subconjunto coplanar por construção. Esse resultado mede somente planaridade; **não comprova melhoria de fidelidade geométrica global**.

A malha A2 local gerada pela projeção possui SHA-256 `43052fdbddfef9949336773e22804f32f4b639072775889d9b61c453accd3345`.

## Bloqueio remanescente da avaliação geométrica A0/A2

O arquivo `raw/study/experiment/mesh_200000/study.ply` do bundle **não é o ground truth DM-SR**. Ele é a malha bruta reconstruída antes da limpeza, como definido no protocolo A0/A1/A2.

A referência geométrica correta é `data/dmsr/study/study.ply`, esperada com:

- 437008 vértices;
- 844701 faces;
- 16225413 bytes;
- SHA-256 `8de1c71689452af874d661b610873a036fddf979b89c86704e5537561c1452fc`.

Portanto, métricas A0/A2 contra ground truth permanecem **PENDENTES** até esse arquivo ser fornecido. Não usar o `study.ply` produzido pelo mesher como referência.

O notebook CPU `notebooks/DMNeRF_Kaggle_CPU_Reference_Pack.ipynb` foi adicionado para obter somente essa referência validada e quatro vistas RGB de teste sem consumir GPU.

## Próxima sequência

1. obter e auditar `dmsr-study-reference-pack.zip` via notebook CPU;
2. executar as métricas geométricas A0 e A2 contra o `study.ply` validado;
3. executar/exportar A0/A1/A2 e G0 no Gazebo;
4. realizar G1–G3 no Gazebo Classic se o ambiente estiver disponível;
5. produzir figuras qualitativas com RGB de entrada, render neural, A0, instâncias A1, piso A1×A2 e Gazebo;
6. agregar evidências e preencher Resultados, Discussão e Conclusão;
7. executar o baseline COLMAP apenas se couber no limite de engenharia definido.
