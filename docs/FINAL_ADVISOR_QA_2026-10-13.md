# QA da versão para o orientador — 13/10/2026

## Artefatos

- PDF: `docs/exports/Dissertacao_Orientador_2026-10-13.pdf`
- fonte LaTeX: `docs/exports/Dissertacao_Orientador_2026-10-13_Fonte_LaTeX.zip`
- diretório fonte: `docs/dissertation/final_advisor_2026-10-13/`
- classe institucional: `texfurg.cls`, fornecida no pacote de entrada

## Resultado da compilação

- formato: A4 (`595.276 × 841.89 pt`);
- páginas: 38;
- figuras: 7;
- tabelas: 11;
- citações indefinidas: zero;
- referências cruzadas indefinidas: zero;
- PDF SHA-256: `b1fa7f4dcfe65983383a7a7c14503b326b5a9aac8abafc4a5caa4febe84661b8`;
- ZIP SHA-256: `de31f834f8ef74d096a8cbe5db6cc34445301e56efb6c114921ec59b26e29261`.

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

Todas as 38 páginas foram renderizadas em PNG e inspecionadas. Foram conferidos margens, cabeçalhos, rodapés, paginação, legibilidade de tabelas, chamadas, legendas, cortes e sobreposições. Não foram observados elementos fora da página, texto sobre área de dados ou figuras ilegíveis.

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

- reduzidos o resumo de 354 para 233 palavras e o abstract de 347 para 228 palavras, preservando problema, método, principais evidências e delimitação das conclusões;
- removidos do resumo e do abstract os códigos internos A0--A2 e G0--G3, contagens de malha e detalhes secundários que pertencem aos capítulos de método e resultados;
- explicitada, antes da primeira utilização técnica e no protocolo, a convenção local: A identifica as condições cumulativas da ablação interna, e G identifica as verificações no Gazebo; esses códigos não pertencem à nomenclatura do DM-NeRF;
- ajustados títulos e rótulos das condições para associar imediatamente A0 à malha, A1 aos objetos e A2 ao piso;
- corrigido o rótulo das palavras-chave em inglês para `Keywords`, sem corte ou extravasamento na página;
- removida a seção “Organização do texto”;
- removidos o parágrafo e a tabela de PQscene, que não contribuíam para a argumentação central;
- substituído “Este trabalho” por “Cadeia DM-NeRF--Gazebo” na comparação qualitativa;
- eliminadas do corpo científico referências a commit, executor, bundle e nomes de arquivos de métricas;
- condensado o capítulo de limitações em quatro parágrafos, preservando as delimitações científicas;
- reduzida a Discussão para 344 palavras em uma única página, concentrada na interpretação dos resultados;
- removido o espaçamento negativo dos rótulos das Figuras 1 e 2; a inspeção em resolução de 120 dpi confirmou que nenhum rótulo é encoberto pelas imagens.
