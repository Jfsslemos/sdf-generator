# QA da versão para o orientador — 13/10/2026

## Artefatos

- PDF: `docs/exports/Dissertacao_Orientador_2026-10-13.pdf`
- fonte LaTeX: `docs/exports/Dissertacao_Orientador_2026-10-13_Fonte_LaTeX.zip`
- diretório fonte: `docs/dissertation/final_advisor_2026-10-13/`
- classe institucional: `texfurg.cls`, fornecida no pacote de entrada

## Resultado da compilação

- formato: A4 (`595.276 × 841.89 pt`);
- páginas: 40;
- figuras: 7;
- tabelas: 11;
- citações indefinidas: zero;
- referências cruzadas indefinidas: zero;
- PDF SHA-256: `7d37886cd36c43d8049828bd41c4b31576fe3edfcc92b77e53dc9b129432f4de`;
- ZIP SHA-256: `189db09a0246c03de71252e6575a001c9b1dac9a235d469fc77d0d0b584bc0c7`.

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

Todas as 40 páginas foram renderizadas em PNG e inspecionadas. Foram conferidos margens, cabeçalhos, rodapés, paginação, legibilidade de tabelas, chamadas, legendas, cortes e sobreposições. Não foram observados elementos fora da página, texto sobre área de dados ou figuras ilegíveis.

Os componentes raster usados nas sete figuras numeradas possuem hashes SHA-256 distintos. A inspeção das páginas confirmou ausência de repetição visual involuntária. A montagem isolada de RGB e a figura isolada de A0 foram removidas; a comparação referência × DM-NeRF apresenta a cena, e a comparação referência DM-SR × DM-NeRF A0 × COLMAP concentra a evidência geométrica. As sublegendas `(a)`, `(b)` e `(c)` ficam fora da imagem.

As Figuras 1 e 2 foram revistas porque referência e predição eram difíceis de distinguir visualmente. A Figura 1 passou a incluir a diferença absoluta por pixel ampliada cinco vezes; a Figura 2 passou a marcar em magenta os pixels com IDs divergentes. As composições originais foram preservadas como fonte, e a derivação das novas linhas está documentada no diretório de figuras.

## Correções verificadas

- COLMAP integrado à introdução, ao protocolo, aos resultados, à discussão e à conclusão;
- contribuição delimitada como avaliação rastreável da cadeia, contrato topologia/IDs, seleção e regularização geométrica e avaliação separada;
- G4 removido do protocolo e do texto científico;
- IoU, AP, MVS e RANSAC explicados; MVS, RANSAC e URDF incluídos na lista de siglas;
- quatro vistas declaradas na figura de instâncias;
- interpretação de G3 limitada ao ponto ensaiado, sem alegação de precisão física micrométrica;
- comparação direta, baseline geométrico próprio e contexto de outros datasets mantidos separados;
- Schönberger e a capitalização de NeRF, DM-NeRF, NeuS, NICE-SLAM, PanoRecon, URDFormer, DRAWER e GRS corrigidos na bibliografia.

## Revisão editorial complementar

- removida a seção “Organização do texto”;
- removidos o parágrafo e a tabela de PQscene, que não contribuíam para a argumentação central;
- substituído “Este trabalho” por “Cadeia DM-NeRF--Gazebo” na comparação qualitativa;
- eliminadas do corpo científico referências a commit, executor, bundle e nomes de arquivos de métricas;
- condensado o capítulo de limitações em quatro parágrafos, preservando as delimitações científicas.
