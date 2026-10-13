# QA da versão para o orientador — 13/10/2026

## Artefatos

- PDF: `docs/exports/Dissertacao_Orientador_2026-10-13.pdf`
- fonte LaTeX: `docs/exports/Dissertacao_Orientador_2026-10-13_Fonte_LaTeX.zip`
- diretório fonte: `docs/dissertation/final_advisor_2026-10-13/`
- classe institucional: `texfurg.cls`, fornecida no pacote de entrada

## Resultado da compilação

- formato: A4 (`595.276 × 841.89 pt`);
- páginas: 41;
- figuras: 7;
- tabelas: 12;
- citações indefinidas: zero;
- referências cruzadas indefinidas: zero;
- PDF SHA-256: `aa9ceff593a3ae58421dd50882d5a233f41146ac63d2367069d0c7dd0d08b70e`;
- ZIP SHA-256: `f60a534ce6b0f35108aa426c28b7f6519556b0d328e5b48a498c103c1721a23d`.

A compilação limpa foi reproduzida por `make`, com `pdflatex`, `bibtex` e duas passagens adicionais de `pdflatex`. O log final não contém warnings de citação ou referência. O registro `Overfull \\hbox` de 17,6 pt ocorre durante `\\maketitle`, na composição herdada da classe institucional; a página de rosto foi inspecionada e não apresenta corte ou sobreposição.

## Varredura de linguagem

O texto foi extraído do PDF final e normalizado para a busca. As expressões abaixo tiveram zero ocorrência com sentido de trabalho incompleto:

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

A busca literal por `pendente` retornou 26 substrings. Todas foram revisadas e pertencem a `independente`, `independentes` ou `independentemente`, inclusive uma ocorrência quebrada entre linhas; não há uso editorial de “pendente”.

## Figuras e inspeção visual

Todas as 41 páginas foram renderizadas em PNG e inspecionadas. Foram conferidos margens, cabeçalhos, rodapés, paginação, legibilidade de tabelas, chamadas, legendas, cortes e sobreposições. Não foram observados elementos fora da página, texto sobre área de dados ou figuras ilegíveis.

As sete figuras usadas possuem hashes SHA-256 distintos. A inspeção das páginas confirmou ausência de repetição visual involuntária. A montagem isolada de RGB e a figura isolada de A0 foram removidas; a comparação referência × DM-NeRF apresenta a cena, e a comparação referência DM-SR × DM-NeRF A0 × COLMAP concentra a evidência geométrica. As sublegendas `(a)`, `(b)` e `(c)` ficam fora da imagem.

## Correções verificadas

- COLMAP integrado à introdução, ao protocolo, aos resultados, à discussão e à conclusão;
- contribuição delimitada como avaliação rastreável da cadeia, contrato topologia/IDs, seleção e regularização geométrica e avaliação separada;
- G4 removido do protocolo e do texto científico;
- IoU, AP, MVS, RANSAC e PQscene explicados; MVS, RANSAC e URDF incluídos na lista de siglas;
- quatro vistas declaradas na figura de instâncias;
- interpretação de G3 limitada ao ponto ensaiado, sem alegação de precisão física micrométrica;
- comparação direta, baseline geométrico próprio e contexto de outros datasets mantidos separados;
- Schönberger e a capitalização de NeRF, DM-NeRF, NeuS, NICE-SLAM, PanoRecon, URDFormer, DRAWER e GRS corrigidos na bibliografia.
