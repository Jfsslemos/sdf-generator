# Estado do pacote para revisão do orientador — 12/10/2026

## Material disponível

O pacote editorial foi gerado a partir de `docs/VERSAO_ORIENTADOR_2026-10-12.md`, com aproximadamente 8.600 palavras. A versão editável e a versão para leitura estão em:

- `docs/exports/Dissertacao_Preliminar_Orientador_2026-10-12.docx` — 330.892 bytes; SHA-256 `ee9431647f687dd0bf8008c41bb3f1e88d9ce7ffa7f69d059a975f62cf215495`;
- `docs/exports/Dissertacao_Preliminar_Orientador_2026-10-12.pdf` — 819.567 bytes; SHA-256 `bbeb5a4e115faec390205cb882921b18cb88dfac7b8e1d90542ccaaf087712f6`.

O PDF possui 32 páginas em formato carta, com capa, sumário, paginação, oito capítulos/seções principais e referências. O DOCX preserva texto, tabelas e imagens de forma editável. A geração é reproduzível por `tools/build_advisor_review.py`; o PDF é obtido pela conversão do DOCX com LibreOffice.

## Estado científico apresentado

A versão separa três estados de evidência:

1. **observado nos registros do Finalize e sujeito à auditoria do bundle:** 200.000 iterações, 199.916 atualizações efetivas, 85 atualizações puladas por AMP, aproximadamente 30 h 58 min de treinamento, picos de memória, tempos de avaliação e meshing, métricas do avaliador oficial em 100 vistas e existência da malha A0;
2. **estabelecido pelo protocolo e pela inspeção dos artefatos disponíveis:** escopo metodológico, condições A0/A1/A2, uso do *bounding frame* da referência no meshing oficial, ausência de rótulo semântico oficial para o piso e separação das famílias de métricas;
3. **ainda não observado:** avaliação geométrica A0, materialização e avaliação de A1, seleção geométrica do piso, A2, validações G1–G4 no Gazebo e baseline COLMAP+dense MVS.

O notebook de geração do pacote de referência em CPU permanece em execução. Nenhum resultado ou imagem dependente dessa etapa foi incluído antecipadamente.

## Figuras incorporadas

Foram incorporadas como imagens, e não apenas como referências de caminho, as cinco figuras metodológicas já disponíveis:

- cadeia metodológica da reconstrução à simulação;
- desenho da ablação A0/A1/A2;
- seleção geométrica e regularização condicionada do piso;
- proveniência e reprodutibilidade dos artefatos;
- resumo descritivo do treinamento científico.

Não foram encontrados no repositório, com proveniência confirmada e prontos para publicação, a montagem RGB da cena `study`, a comparação referência × render ou vistas renderizadas da malha A0. O texto reserva três posições editoriais para essas figuras e as identifica como material ainda não incorporado, sem usar imagens sintéticas como evidência.

## Verificações realizadas

- renderização integral do DOCX para PDF e PNG;
- inspeção visual das 32 páginas renderizadas, incluindo capa, sumário, tabela comparativa em paisagem, figuras, tabelas numéricas, paginação e referências;
- verificação de integridade do contêiner DOCX;
- confirmação de cinco imagens incorporadas ao DOCX;
- conferência de existência e correspondência das chamadas das Figuras 1–8 e Tabelas 1–4;
- conferência das citações do texto contra a lista de referências;
- remoção do DOI de URDFormer que aparecia com o marcador não verificável `XX`, sem substituição por dado inferido;
- busca por marcadores repetitivos `PENDENTE`, caminhos absolutos de máquina e comentários operacionais no corpo científico;
- confirmação de que o sumário coincide com as páginas iniciais das seções.

## Diferenças para a versão final destinada à banca

A versão atual foi preparada para leitura crítica do argumento, do enquadramento na literatura, da metodologia e dos resultados parciais. A versão final para a banca deverá, quando houver evidência, incorporar:

1. auditoria do bundle final e confirmação rastreável das métricas observadas no Finalize;
2. figuras qualitativas reais da entrada, da renderização e da malha A0;
3. métricas geométricas da malha A0 contra a referência DM-SR;
4. resultados de A1, seleção do piso e A2, respeitando eventual ambiguidade ou abstenção da heurística;
5. validação funcional no Gazebo e, somente se efetivamente executado, resultado do baseline COLMAP+dense MVS.

Os dados institucionais completos da folha de rosto — instituição, programa, orientador e local — não foram encontrados nas fontes consultadas e não foram inventados. A capa identifica o autor, o título provisório, a natureza do documento e a data; a normalização institucional deverá ser aplicada quando esses dados forem fornecidos.
