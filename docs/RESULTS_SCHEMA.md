# Schema rastreável dos resultados

`tools/aggregate_results.py` transforma um diretório de artefatos em quatro
arquivos derivados, sem executar modelos e sem completar lacunas com valores
históricos. O agregador usa somente a biblioteca padrão do Python.

```bash
python tools/aggregate_results.py results/final-study \
  --output results/final-study/derived_summary
```

O diretório de saída pode ficar dentro da entrada: ele é excluído da descoberta,
o que torna a reexecução idempotente. Os caminhos registrados são relativos à
raiz de entrada. Cada fonte utilizada aparece em `summary.json/sources` com
SHA-256, tamanho e papéis. Não há timestamp de geração, de modo que entradas
idênticas geram bytes idênticos.

## Estados

| Estado | Interpretação |
|---|---|
| `AVAILABLE` | Existe artefato válido que sustenta o valor ou resultado. |
| `PENDING` | O dado esperado ainda não foi encontrado. O valor permanece `null`. |
| `NOT_EXECUTED` | A evidência declara que a execução não ocorreu, ou o baseline não possui relatório real. |
| `NOT_APPLICABLE` | O protocolo determina que o campo não se aplica à condição. |

Zero é aceito somente quando está escrito em uma fonte válida — por exemplo,
zero skips AMP ou utilização zero da segunda GPU. Zero nunca é usado como
substituto de ausência. Strings vazias não são métricas. `NaN`, infinito,
JSON/CSV malformado, fontes finais conflitantes e métricas ambíguas interrompem
a execução.

## Descoberta e precedência

| Artefato | Campo/família | Regra |
|---|---|---|
| `training_state.json` | iteração final, target, updates, skips, estado de conclusão, pico PyTorch | Prefere paths com componente `experiment`; exclui smoke, piloto e benchmark. Entre checkpoints, usa a maior iteração e rejeita estados conflitantes na mesma iteração. |
| `training.jsonl` | tempo observado, throughput, segmentos de processo e pico PyTorch | Soma o último `elapsed_seconds` de cada processo detectado. Valida sequência e contadores; cópias sobrepostas são rejeitadas. |
| `stages.jsonl` | duração e estado de train/evaluate/mesh | Deduplica snapshots pelo timestamp, nome da etapa e log. Não soma esse tempo ao tempo do treino. |
| `*-gpu.csv` | pico de memória e utilização média por GPU | Lê a telemetria `nvidia-smi`. GPUs de mesmo modelo são separadas por ordinal em cada amostra. |
| `derived/experiment/metrics.csv` | PSNR, SSIM, LPIPS e AP50/75/80/85/90/95 | Usa exatamente a linha `mean` do evaluator oficial e exige ao menos uma linha de vista. Escopo sempre `test`. |
| JSON com assinatura de `evaluate_mesh_distance.py` | Precision, Completeness, F-score e distâncias direcionais/simétrica | Preserva os limiares nos próprios nomes (`precision@0.01`, etc.). Condição vem de token A0/A1/A2/baseline no path; sem token fica `unassigned`. |
| JSON com assinatura de `evaluate_planarity.py` | média absoluta, RMSE, P95 e inlier fraction | Mantém cada avaliação como registro separado e conserva o seletor. |
| relatório de `regularize_floor.py` | métricas antes/depois e fração de inliers RANSAC | Preserva o relatório pareado; não o confunde com uma avaliação independente posterior. |
| `floor_selection.json` | ID selecionado, tipo da evidência e flag semântica | O ID continua declarado como heurística geométrica, nunca ground truth semântico. |
| `instances.json` | contagem, cobertura e faces de fronteira | Evidência estrutural de A1/A2; não produz métricas de imagem. |
| `gazebo_validation.json` | G0–G4 | `PASS`/`FAIL` são valores `AVAILABLE`; `NOT_EXECUTED` e `NOT_APPLICABLE` permanecem estados explícitos. |
| `baseline_run.json` | execução COLMAP | Só marca baseline disponível quando o relatório real contém `status=ok`. Métricas geométricas do baseline continuam exigindo saída de avaliação de mesh. |

Se houver mais de um `metrics.csv`, `floor_selection.json` ou relatório COLMAP
com conteúdo diferente, a execução falha. Isso evita selecionar silenciosamente
um resultado conveniente. Smoke, piloto e benchmark AMP não entram como
resultado científico final.

## Campos de `summary.json`

- `training`: escopo `train`; progresso, updates/skips, tempo, throughput, VRAM,
  telemetria e etapas registradas.
- `test_evaluation`: escopo `test`; `rendering` e `decomposition`. Nenhum campo
  lido do log de treino pode alimentar esta seção.
- `geometry.records`: um registro por relatório geométrico, com condição, fonte
  e métricas nos limiares efetivamente encontrados.
- `ablation.floor`: seleção, avaliações de planaridade e relatório pareado da
  regularização.
- `ablation.instance_structure`: manifestos de instâncias por condição.
- `gazebo.conditions`: matriz A0/A1/A2 × G0–G4 conforme aplicabilidade congelada.
- `baseline`: execução COLMAP somente quando houver relatório real.
- `sources`: inventário canônico das evidências utilizadas.

Cada métrica de cardinalidade fixa é um objeto com `status`, `value`, `sources`
e, quando aplicável, `unit`/`note`. Métricas geométricas com limiares dinâmicos
ficam em `records[].metrics` e carregam uma fonte no próprio registro.

## Saídas

- `summary.json`: estrutura completa e proveniência.
- `summary.csv`: uma linha por campo/métrica, adequada para auditoria e filtros.
- `tables.md`: tabelas de treinamento, teste, geometria, piso, instâncias,
  Gazebo e baseline; ausência aparece como travessão.
- `results_status.md`: status por família e por campo, incluindo a fonte.

O CSV e as tabelas são derivados. Os artefatos brutos permanecem separados e
são a autoridade para qualquer conferência.

