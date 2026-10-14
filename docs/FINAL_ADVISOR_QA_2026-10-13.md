# QA da versão para o orientador — revisão de 14/10/2026

## Artefatos

- PDF: `docs/exports/Dissertacao_Orientador_2026-10-14.pdf`
- fonte LaTeX: `docs/exports/Dissertacao_Orientador_2026-10-14_Fonte_LaTeX.zip`
- diretório fonte: `docs/dissertation/final_advisor_2026-10-13/`
- classe institucional: `texfurg.cls`, fornecida no pacote de entrada

## Resultado da compilação

- formato: A4 (`595.276 × 841.89 pt`);
- páginas: 39;
- figuras: 8;
- tabelas: 11;
- citações indefinidas: zero;
- referências cruzadas indefinidas: zero;
- PDF SHA-256: `1984965cd8ddc1e71cb6279ca2a687131190268beedda7779e859d40e98abd7f`;
- ZIP SHA-256: `2d142426c9030e400ad77ab0df1a6113b7fd423f39d88b7bffc24204052bc7b7`.

A compilação limpa foi reproduzida por `make`, com `pdflatex`, `bibtex` e duas passagens adicionais de `pdflatex`. O log final não contém avisos de citação ou referência. O registro `Overfull \\hbox` de 17,6 pt ocorre durante `\\maketitle`, na composição herdada da classe institucional; a página de rosto foi inspecionada e não apresenta corte nem sobreposição.

## Verificações editoriais e científicas

- título definitivo aplicado à capa, folha de rosto e metadados do PDF: **Reconstrução Semântica Automatizada de Ambientes Domésticos para Simulação de Robôs**;
- cabeçalho do resumo em inglês corrigido para `ABSTRACT`;
- discussão ampliada para relacionar a cadeia experimental a DM-NeRF, Panoptic Neural Fields, Panoptic Lifting, PanoRecon, URDFormer, DRAWER, GRS e COLMAP, sem alegação de superioridade geral;
- subseção curta de validade incluída com os limites da cena, supervisão, meshing, COLMAP, malhas, piso, planarização e ensaio G3;
- contribuição apresentada como a passagem medida entre representação neural, geometria explícita, objetos independentes e cena de simulação;
- publicação anterior do autor relacionada à origem do problema e à prova de conceito, sem combinar seus resultados com as medições atuais;
- referências de SSIM, LPIPS e RANSAC incluídas; PSNR, IoU e AP vinculados ao protocolo do DM-NeRF;
- reprodutibilidade vinculada ao repositório público, e custo interpretado como preparação offline da cena;
- conclusão reescrita para responder à expressão “em que medida”, sem resposta binária.

## Figuras e inspeção visual

Todas as 39 páginas foram renderizadas em PNG e inspecionadas. Foram conferidos margens, cabeçalhos, rodapés, paginação, sumário, listas, tabelas, chamadas, legendas, cortes e sobreposições. A nova figura metodológica foi criada em SVG editável e exportada para PDF; sua versão final não contém texto cortado. A tabela comparativa de trabalhos relacionados foi reorganizada em três colunas para melhorar a leitura.

Os 12 arquivos usados em figuras possuem hashes SHA-256 distintos. A comparação perceptual encontrou apenas dois pares próximos: referência × renderização neural e máscara de referência × máscara predita. Em ambos os casos, a semelhança é o próprio objeto da comparação científica; não há repetição acidental. Nenhuma vista sintética foi criada.

## Varredura de linguagem

O texto foi extraído do PDF final. As expressões abaixo tiveram zero ocorrência com sentido de trabalho incompleto:

- “não integra”;
- “quando o runtime”;
- “ainda necessária”;
- “resultados disponíveis”;
- “não executado”;
- “trabalho futuro”;
- “como continuidade”;
- “se for executado”;
- “pendente”;
- “a realizar”;
- “será avaliado”;
- “será executado”;
- “quando houver”.

A busca literal por `pendente` encontra apenas o interior de `independente`, `independentes` e `independentemente`. Não há linguagem de relatório de andamento no corpo científico.
