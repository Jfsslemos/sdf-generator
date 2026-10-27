# Resultados — estrutura de redação

Este arquivo define a estrutura da seção de Resultados antes da conclusão do
experimento. `PENDING` indica ausência de evidência final agregada; não é zero,
falha nem estimativa. As tabelas finais devem ser substituídas pelas geradas em
`tables.md`, preservando as fontes de `summary.json`.

## 1. Execução e custo computacional

Relatar ambiente, checkpoint final, número de updates efetivos, skips AMP,
tempo observado, throughput e memória. Separar tempo de treino das etapas de
avaliação e meshing; não somar `stage_seconds` ao treino quando os intervalos se
sobrepõem.

| Iteração final | Updates efetivos | Skips AMP | Tempo de treino | s/it | Pico VRAM |
|---:|---:|---:|---:|---:|---:|
| PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |

Não interpretar piloto, benchmark AMP ou sessão parcial como resultado final.

## 2. Síntese de vistas e decomposição

Esta subseção usa apenas `derived/experiment/metrics.csv`, produzido pelo
evaluator oficial sobre o conjunto de teste. Loss e logs de treinamento não
entram nesta tabela.

| PSNR | SSIM | LPIPS | AP50 | AP75 | AP80 | AP85 | AP90 | AP95 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |

Descrever os valores somente após o evaluator final. Não antecipar ganho sobre
outros métodos sem executar uma comparação compatível.

## 3. Avaliação geométrica

Declarar que o meshing oficial usa o bounding frame da referência DM-SR. Fixar
e informar a amostragem e os limiares já previstos no protocolo.

| Condição/método | Limiar | Precision | Completeness | F-score | Pred→GT | GT→Pred | Distância simétrica |
|---|---:|---:|---:|---:|---:|---:|---:|
| A0 | 1 cm | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| A0 | 2 cm | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| A0 | 5 cm | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |

A1 não recebe uma alegação de melhoria geométrica apenas por separar arquivos.
A2 só deve ser incluída se a regularização realmente alterar a geometria
avaliada. COLMAP entra apenas se houver reconstrução e avaliação reais.

## 4. Ablation A0/A1/A2

Apresentar cada condição apenas nas propriedades que ela pode alterar:

- A0: geometria neural bruta e integração básica;
- A1: individualização estrutural das instâncias;
- A2: A1 mais regularização geométrica do piso.

| Condição | Evidência estrutural | Geometria | Piso | Gazebo |
|---|---|---|---|---|
| A0 | PENDING | PENDING | NOT_APPLICABLE | PENDING |
| A1 | PENDING | não atribuir ganho automaticamente | PENDING (antes) | PENDING |
| A2 | PENDING | PENDING se avaliada | PENDING (depois) | PENDING |

## 5. Regularização do piso

Registrar `floor_selection.json` e explicitar que a seleção é uma heurística
geométrica, não ground truth semântico. Comparar o mesmo subconjunto antes e
depois; P95 é a medida primária.

| Estado | Média absoluta | RMSE | P95 | Fração de inliers |
|---|---:|---:|---:|---:|
| Antes (A1) | PENDING | PENDING | PENDING | PENDING |
| Depois (A2) | PENDING | PENDING | PENDING | PENDING |

Não escrever que o piso foi identificado ou melhorado enquanto o seletor tiver
abstido ou os relatórios finais não existirem.

## 6. Validação funcional no Gazebo Classic

| Condição | G0 | G1 | G2 | G3 | G4 |
|---|---|---|---|---|---|
| A0 | PENDING | PENDING | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE |
| A1 | PENDING | PENDING | PENDING | NOT_APPLICABLE | NOT_APPLICABLE |
| A2 | PENDING | PENDING | PENDING | PENDING | PENDING/NOT_EXECUTED |

G0 é apenas validação estática. Sucesso no Gazebo não substitui métricas
geométricas ou de imagem. Preservar warnings mesmo quando um gate passar.

## 7. Baseline COLMAP

| Execução | Geometria avaliada | Fonte |
|---|---|---|
| NOT_EXECUTED | PENDING | PENDING |

Esta subseção só recebe números se `baseline_run.json` provar uma execução real
e a saída for avaliada pelo mesmo protocolo geométrico. Preparação de inputs,
teste CPU ou existência do notebook não constituem resultado do baseline.

## 8. Limitações observadas

Preencher após os resultados, restringindo-se a evidências registradas. Manter,
independentemente dos valores finais, as limitações já definidas: dependência do
bounding frame oficial, ausência de semântica oficial do piso e distinção entre
fidelidade geométrica, decomposição e utilidade no simulador.

