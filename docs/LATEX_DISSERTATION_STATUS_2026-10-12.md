# Estado da dissertação em LaTeX — 12/10/2026

## Fonte institucional

O template LaTeX do PPGComp/FURG fornecido pelo autor foi adotado como fonte principal da versão da dissertação. A classe utilizada é `texfurg` com as opções `dm,ppgcomp,nocipinfo`. A ficha catalográfica e a composição da banca não foram preenchidas nesta etapa porque os dados completos ainda não foram fornecidos; nenhum placeholder institucional foi inventado.

## Auditoria científica concluída

O bundle final pós-Finalize e o reference pack do DM-SR foram auditados antes da incorporação dos resultados.

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
- 200.000 amostras de superfície, seed 42;
- F-score: 0,0480 a 1 cm, 0,1960 a 2 cm e 0,7750 a 5 cm;
- média predição->referência: 4,335 cm;
- média referência->predição: 4,139 cm;
- distância L1 simétrica: 8,474 cm.

A1:
- 13 instâncias com faces exportáveis;
- 681.383 faces homogêneas;
- 29.545 faces de fronteira;
- cobertura de faces homogêneas: 95,844%.

Piso/A2:
- seletor geométrico congelado selecionou `instance_id=10`, sem escolha manual;
- a evidência permanece declarada como heurística geométrica, não ground truth semântico;
- A1: média absoluta 2,051 cm, RMSE 5,722 cm, P95 6,800 cm, 77,11% de inliers a 2 cm;
- A2: resíduos numéricos próximos de zero após a projeção, resultado interpretado apenas como planarização por construção.

## Gazebo

G0 passou para A0, A1 e A2. A0 gera um modelo; A1 e A2 geram 13 modelos com referências locais válidas. As malhas não são estanques, portanto G3 continua necessário.

G1, G2 e G3 dependem do runtime do Gazebo Classic e permanecem não executados no ambiente de elaboração atual, que não possui `gazebo`, `gzserver` ou `gz`.

Foi preparado um pacote reproduzível para que esses três testes sejam executados em uma máquina com Gazebo Classic. G4 continua opcional e não bloqueia a dissertação.

## Figuras

A nova versão privilegia material qualitativo derivado dos dados reais:
- quatro vistas RGB da cena study;
- referência x render final em quatro vistas;
- máscaras de instância de referência x predição;
- duas vistas da geometria A0;
- duas vistas da decomposição A1;
- quatro instâncias isoladas;
- comparação visual A1 x A2 do candidato a piso.

Os infográficos anteriores de treinamento, proveniência e ablação não foram utilizados como núcleo visual do documento.

## Estado editorial

A versão LaTeX compilada contém 36 páginas A4 e foi renderizada integralmente para inspeção visual. Não foram encontrados placeholders `PENDENTE`, referências/citações indefinidas, figuras cortadas ou texto saindo de caixas. O único aviso de overfull restante é produzido durante `\maketitle` pela classe institucional e não apresentou corte visível na página renderizada.

Antes do envio final para a banca ainda faltam:
1. G1/G2/G3 no Gazebo Classic e respectivas evidências;
2. incorporar as capturas reais do Gazebo;
3. validar o título definitivo com o orientador;
4. preencher banca e ficha catalográfica quando os dados estiverem disponíveis.

COLMAP permanece opcional e não deve atrasar essas etapas.
