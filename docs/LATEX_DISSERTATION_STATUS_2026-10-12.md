# Estado da dissertação em LaTeX — atualizado em 13/10/2026

## Fonte institucional

O template LaTeX do PPGComp/FURG fornecido pelo autor foi adotado como fonte principal da versão da dissertação. A classe utilizada é `texfurg` com as opções `dm,ppgcomp,nocipinfo`. A ficha catalográfica e a composição da banca permanecem sem preenchimento porque os dados completos ainda não foram fornecidos; nenhum placeholder institucional foi inventado.

## Auditoria científica concluída

O bundle final pós-Finalize e o reference pack do DM-SR foram auditados.

Resultados do avaliador oficial sobre 100 vistas de teste:
- PSNR: 41,1100 dB;
- SSIM: 0,9875;
- LPIPS: 0,0260;
- AP50: 0,9956;
- AP75: 0,9911;
- AP80: 0,9849;
- AP85: 0,9769;
- AP90: 0,9311;
- AP95: 0,7192.

Geometria A0:
- 356.272 vértices e 710.928 faces;
- F-score: 0,0480 a 1 cm, 0,1960 a 2 cm e 0,7750 a 5 cm;
- média predição->referência: 4,335 cm;
- média referência->predição: 4,139 cm;
- distância L1 simétrica: 8,474 cm.

A1:
- 13 instâncias com faces exportáveis;
- 681.383 faces homogêneas;
- 29.545 faces de fronteira;
- cobertura: 95,844%.

Piso/A2:
- seletor geométrico selecionou `instance_id=10`, sem escolha manual;
- A1: média absoluta 2,051 cm, RMSE 5,722 cm, P95 6,800 cm, 77,11% de inliers a 2 cm;
- A2: resíduos próximos de zero após projeção, interpretados apenas como planarização por construção.

## Gazebo Classic

Runtime executado no Gazebo Classic 11.10.2.

- G0: PASS para A0, A1 e A2;
- G1: PASS para A0, A1 e A2;
- G2: PASS em A1, com deslocamento independente de `instance_006`;
- G3: PASS em A2 após auditoria do teste;
- G4: não executado e opcional.

Em G3, o mundo define uma caixa de 10 cm com centro inicial em `z=0.65 m`. O script original espera seis segundos antes da primeira consulta e por isso registrou como “inicial” uma pose já posterior ao assentamento. A primeira pose medida foi `z=0.093811 m` e, oito segundos depois, `z=0.093806 m`. A face inferior da caixa ficou em `z=0.043806 m`, enquanto o plano regularizado prevê aproximadamente `z=0.043810 m` no mesmo ponto. A diferença é inferior a 4 micrômetros. O “INCONCLUSIVO” automático do script foi, portanto, decorrente da lógica de coleta e não de falha de contato.

A interpretação completa está registrada em `docs/GAZEBO_RUNTIME_RESULTS_2026-10-13.md`.

## Figuras

A versão atual utiliza material qualitativo derivado dos dados reais:
- quatro vistas RGB da cena study;
- referência x render final;
- mapas de instância GT x predição;
- visualizações A0;
- decomposição A1;
- instâncias isoladas;
- A1 x A2 do piso;
- captura real da condição A2 no Gazebo durante G3.

## Estado editorial

A versão LaTeX atualizada contém 38 páginas A4 e foi recompilada e renderizada após a incorporação de G1--G3. Não há referências/citações indefinidas. O aviso de overfull restante ocorre em `\maketitle` na classe institucional e não apresentou corte visível.

Pendências para a versão de banca:
1. validar o título definitivo com o orientador;
2. preencher banca e ficha catalográfica quando os dados estiverem disponíveis;
3. revisão editorial final após feedback do orientador.

COLMAP e G4 permanecem opcionais e não devem atrasar o fechamento.
