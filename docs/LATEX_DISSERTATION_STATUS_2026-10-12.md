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

## Comparações externas

A comparação com a literatura inclui:
- reprodução direta do DM-NeRF na mesma cena `study`, confrontada com os valores publicados de PSNR, SSIM, LPIPS e AP0.75;
- Mask R-CNN e Swin Transformer conforme os valores de AP0.75 publicados por Wang et al. no mesmo experimento;
- contexto quantitativo de métodos panópticos posteriores em seus próprios benchmarks, explicitamente separado da comparação direta por diferenças de datasets e métricas;
- baseline geométrico externo COLMAP+dense MVS executado sobre a mesma cena.

O COLMAP foi executado com 300 vistas, 10 fontes por referência, consistência geométrica, faixa de profundidade 4--15 m e `StereoFusion.min_num_pixels=1`. A fusão gerou 5.800.316 pontos.

A avaliação escrita diretamente pelo notebook COLMAP foi descartada para a dissertação porque não era diretamente comparável a A0: o COLMAP estava no sistema das poses DM-SR e sem o mesmo suporte espacial/cardinalidade usado pelo mesher do DM-NeRF.

A auditoria final:
- converte COLMAP para o sistema de cena por `scene=[x,z,-y]`;
- restringe a nuvem ao mesmo suporte orientado `[1.9,7.0,7.0]` m usado pelo mesher upstream;
- usa 200.000 pontos por conjunto e seed 42.

Dos 5.800.316 pontos, 3.416.962 (58,91%) ficam no suporte comum.

Resultados comparáveis A0 x COLMAP:
- F-score @1 cm: 0,0480 x 0,0285;
- F-score @2 cm: 0,1960 x 0,1288;
- F-score @5 cm: 0,7750 x 0,3721;
- L1 simétrica: 8,474 cm x 28,547 cm;
- média predição->referência: 4,335 cm x 20,418 cm;
- média referência->predição: 4,139 cm x 8,129 cm.

A interpretação e o protocolo estão registrados em `docs/COLMAP_BASELINE_AUDIT_2026-10-13.md`. Os números não são usados para alegar superioridade geral do DM-NeRF sobre COLMAP; tratam-se de uma cena, uma configuração fixa e poses fornecidas.

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
- quatro vistas RGB da cena `study`;
- referência x render final;
- mapas de instância GT x predição;
- comparação geométrica referência x A0 x COLMAP no mesmo sistema;
- gráfico de F-score A0 x COLMAP;
- decomposição A1 colorida por instância;
- resíduos do piso A1 x A2;
- captura real e colorida da condição A2 no Gazebo durante G3.

As figuras que apresentavam texto rasterizado sobre os dados, visualização A0 excessivamente densa, instâncias isoladas ruidosas e captura cinza do Gazebo foram retiradas do caminho editorial.

## Estado editorial

A versão LaTeX atualizada contém 41 páginas A4 e foi recompilada e renderizada após a incorporação do baseline COLMAP e das figuras corrigidas. Não há referências/citações indefinidas. O aviso de overfull restante ocorre em `\maketitle` na classe institucional e não apresentou corte visível.

Pendências para a versão de banca:
1. validar o título definitivo com o orientador;
2. preencher banca e ficha catalográfica quando os dados estiverem disponíveis;
3. revisão editorial final após feedback do orientador.

O baseline COLMAP está concluído. G4 permanece opcional e não deve atrasar o fechamento.


## Revisão em modo de banca — 13/10/2026, após a compilação acima

A compilação de 41 páginas **não deve ser tratada como pronta para envio final ao orientador** antes das correções abaixo:

- seção 1.3 ainda afirma que o COLMAP não integra os resultados;
- seção 1.4 ainda fala em etapas necessárias para fechar a avaliação funcional;
- seção 4.2 ainda usa o condicional “quando o runtime estiver disponível”;
- seção 5.3 diz que a Figura 3 contém três vistas, enquanto a figura contém quatro;
- seção 5.4 diz que a Figura 4 contém duas vistas, enquanto a versão atual contém uma;
- a referência de Schönberger aparece no PDF como `Sch"onberger`;
- a diferença numérica de ~4 µm observada em G3 deve ser descrita como consistência entre pose registrada e plano calculado, não como precisão física micrométrica do Gazebo.

A Figura 5 já fornece comparação qualitativa Referência x A0 x COLMAP. Para leitores não especialistas, recomenda-se adicionar subcaptions externos aos três painéis e, se possível, uma segunda vista/detalhe da mesma região, sempre sem texto sobreposto à área de dados.

Parecer completo: `docs/BANCA_REVIEW_2026-10-13.md`.
