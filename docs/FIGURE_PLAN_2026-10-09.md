# Plano de figuras e tabelas — versão para revisão do orientador

Este plano organiza o material visual do draft sem antecipar resultados ainda não produzidos. Diagramas metodológicos usam apenas decisões e fatos já registrados. Figuras derivadas da avaliação, da malha final ou do Gazebo permanecem condicionadas à etapa **Finalize**.

## Figuras disponíveis para a versão de revisão

| Figura | Prioridade | Inserção no texto | Legenda proposta | Origem dos dados ou artefatos | Estado |
|---|---|---|---|---|---|
| 1 — Cadeia metodológica | **ESSENCIAL** | Seção 3.1, após a separação dos três níveis de evidência | **Visão geral da cadeia metodológica, desde as entradas do DM-SR até a avaliação e a geração das condições A0, A1 e A2 para integração no Gazebo Classic.** | `DRAFT_ORIENTADOR_2026-10-09.md`, `EXPERIMENT_PLAN.md`, protocolo oficial descrito no draft | **PRONTA** — SVG editável e PNG |
| 2 — Ablação A0/A1/A2 | **ESSENCIAL** | Seção 3.5, após a discussão sobre o que a separação estrutural pode alterar; detalhada novamente na Seção 4.2 | **Condições encadeadas da ablação e famílias de evidência pertinentes a cada transformação.** | `ABLATION_PROTOCOL.md`, `RESULTS_DRAFT.md` | **PRONTA** — SVG editável e PNG |
| 3 — Piso: seleção e regularização | **ESSENCIAL** | Seção 3.7, após a descrição da avaliação pareada | **Fluxo da heurística geométrica de seleção do candidato a piso, incluindo os estados de abstenção e a regularização condicionada.** | `FLOOR_IDENTIFICATION.md`, `ABLATION_PROTOCOL.md` | **PRONTA** — SVG editável e PNG |
| 4 — Proveniência | **DESEJÁVEL** | Seção 4.8, após as regras para dados ausentes e fontes conflitantes | **Encadeamento de proveniência entre fontes primárias, identidade da execução, artefatos derivados e evidências consolidadas.** | `DRAFT_ORIENTADOR_2026-10-09.md`, `RESULTS_DRAFT.md`, `WORK_STATUS.md` | **PRONTA** — SVG editável e PNG |
| 5 — Resumo do treinamento | **DESEJÁVEL** | Seção 5.1, antes da tabela de custo computacional | **Resumo descritivo da execução científica concluída em três sessões, sem inclusão de métricas de avaliação ou de teste.** | Estado final confirmado do treinamento: 3 sessões, 200.000 iterações, 199.916 atualizações efetivas, 85 atualizações puladas por AMP, aproximadamente 30 h 58 min e pico PyTorch aproximado de 5,58 GiB | **PRONTA** — SVG editável e PNG; não depende do Finalize |

Os arquivos editáveis são mantidos em `docs/figures/*.svg`. As versões `*.png` destinam-se à visualização rápida e à futura importação em editores que não preservem SVG.

## Tabelas recomendadas

As tabelas já estruturadas na Seção 5 devem permanecer sem valores enquanto não houver evidência final. Para a revisão do orientador, recomenda-se conservar:

1. execução e custo computacional;
2. síntese de vistas e decomposição;
3. métricas geométricas por limiar e distâncias direcionais;
4. cobertura da separação de instâncias;
5. identificação e regularização do piso;
6. validação G0–G4; e
7. síntese da ablação A0/A1/A2.

Não se recomenda transformar essas tabelas em gráficos antes da consolidação dos dados, pois os campos ainda ausentes não devem ser representados como zero, estimativa ou resultado histórico.

## Figuras dependentes do Finalize

| Material futuro | Prioridade | Dependência objetiva | Inserção prevista |
|---|---|---|---|
| Render da malha final A0, com vista e enquadramento documentados | **FINAL** | `mesh_geometry.ply` final | Seção 5.3 |
| Visualização da decomposição e das instâncias separadas A1 | **FINAL** | `instance_labels.npz`, `instances.json` e meshes exportadas | Seção 5.4 |
| Comparação visual pareada do piso A1 × A2 | **FINAL** | seleção válida em `floor_selection.json` e malha regularizada | Seção 5.5 |
| Diagnóstico quantitativo dos resíduos do piso antes/depois | **FINAL** | relatórios finais de planaridade e regularização | Seção 5.5 |
| Capturas reproduzíveis do Gazebo Classic para G1–G3 e eventual G4 | **FINAL** | mundo final carregado e gates executados | Seção 5.6 |
| Gráficos finais de síntese, decomposição, geometria e custo | **FINAL** | métricas agregadas e respectivas fontes validadas | Seções 5.1–5.3 |

Esses materiais não devem ser substituídos por ilustrações sintéticas ou por artefatos do piloto. Caso uma etapa permaneça não executada ou não aplicável, sua ausência deve ser declarada no texto e na tabela correspondente.

## Figuras qualitativas do processo e dos resultados

O texto final deve mostrar a evolução visual da cena, e não apenas diagramas metodológicos. Essas figuras têm prioridade alta porque permitem ao leitor verificar qualitativamente o que entra na cadeia, o que é reconstruído, como a estrutura por instâncias é materializada e como a cena chega ao simulador. Sempre que possível, usar o mesmo enquadramento ou vistas comparáveis para facilitar a leitura.

| Material qualitativo | Prioridade | Conteúdo esperado | Dependência | Inserção prevista |
|---|---|---|---|---|
| Montagem da cena de entrada | **ESSENCIAL** | 4–6 vistas RGB representativas da cena *study*, identificadas como entradas do DM-SR | imagens originais do dataset | Seção 3.2 |
| Comparação GT × síntese neural | **DESEJÁVEL** | 2–4 vistas de teste lado a lado, referência e render final, sem usar PSNR de treino | saída do evaluator final | Seção 5.2 |
| Malha reconstruída A0 | **ESSENCIAL** | render da malha completa, preferencialmente em 2 vistas documentadas | mesh final | Seção 5.3 |
| Decomposição/instâncias A1 | **ESSENCIAL** | cena colorida por instância e exemplos de 3–5 objetos isolados reconstruídos | labels + meshes A1 | Seção 5.4 |
| Piso A1 × A2 | **ESSENCIAL se A2 existir** | comparação lado a lado da geometria antes/depois, com mesmo ponto de vista e zoom da superfície | seleção válida + regularização | Seção 5.5 |
| Cena final no Gazebo | **ESSENCIAL** | captura geral da cena carregada; idealmente uma segunda imagem com objeto manipulado/removido ou robô inserido | G1/G2 e mundo final | Seção 5.6 |
| Figura-síntese do processo | **DESEJÁVEL** | painel compacto: entrada RGB → A0 → A1 → A2 (se aplicável) → Gazebo | resultados qualitativos acima | início da Seção 5 ou Considerações finais |

Para os exemplos de objetos reconstruídos, selecionar instâncias visualmente informativas somente após a geração real das malhas. A seleção deve ser apresentada como ilustração qualitativa e não como escolha estatística ou evidência de desempenho. Não ocultar falhas relevantes da reconstrução em favor de exemplos exclusivamente favoráveis.

## Convenção visual adotada

- fundo claro, tipografia sem serifa e contraste adequado para impressão;
- azul para o estágio neural, verde para geometria e estrutura, roxo para simulação e laranja para avaliação ou gates;
- setas contínuas para transformação de artefatos e tracejadas para avaliação, validação ou vínculo de proveniência;
- legendas autossuficientes, com indicação de elaboração própria;
- nenhuma cor ou forma é usada para sugerir superioridade entre A0, A1 e A2.
