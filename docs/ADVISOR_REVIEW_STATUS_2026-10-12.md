# Estado do pacote para revisão do orientador — atualizado em 13/10/2026

## Situação atual

O pacote de 12/10 está obsoleto e não deve mais ser enviado ao orientador. O experimento principal foi fechado depois daquela versão.

A versão LaTeX local mais recente tem 41 páginas e já incorpora:
- reprodução auditada do DM-NeRF em 100 vistas de teste;
- geometria A0 contra a referência DM-SR;
- separação A1;
- seleção/regularização A2;
- G0--G3 no Gazebo Classic;
- baseline COLMAP+dense MVS executado nas 300 vistas;
- comparação quantitativa A0 x COLMAP no mesmo suporte;
- figuras qualitativas reais de renderização, instâncias, geometria e Gazebo.

O baseline COLMAP está auditado em `docs/COLMAP_BASELINE_AUDIT_2026-10-13.md`, com script reproduzível em `tools/baselines/audit_colmap_common_support.py` e métricas derivadas em `docs/exports/colmap_common_support_metrics.json`.

## Estado científico

A pergunta central está respondida apenas para a cena `study`: a reconstrução DM-NeRF decomposta pôde ser transformada em modelos independentes, carregados no Gazebo e usados em um ensaio pontual de apoio/colisão.

A comparação externa não é apresentada como ranking geral:
- A0 supera a execução COLMAP nos F-scores de 1/2/5 cm sob o protocolo comum;
- o COLMAP usa poses fornecidas e uma configuração fixa;
- o estudo continua restrito a uma cena;
- o meshing do DM-NeRF depende do bounding frame da referência.

## Figuras qualitativas existentes

A versão atual possui:
1. RGB de entrada;
2. referência x render DM-NeRF;
3. mapas de instância referência x predição;
4. visualização A0;
5. referência DM-SR x A0 x COLMAP no mesmo sistema/enquadramento;
6. F-score A0 x COLMAP;
7. A1 colorida por ID;
8. resíduos do piso antes/depois;
9. captura real do Gazebo com instâncias coloridas.

Não há texto sobreposto às áreas de dados nas figuras atuais.

## Correções editoriais obrigatórias antes do envio

A revisão em modo de banca encontrou inconsistências que tornam a versão de 13/10 ainda inadequada para envio como texto final:

1. seção 1.3 ainda afirma que o COLMAP não integra os resultados, apesar de o Capítulo 5 já conter o baseline;
2. seção 1.4 ainda fala em “resultados disponíveis” e “etapas ainda necessárias para fechar a avaliação funcional”, embora G1--G3 tenham sido executados;
3. seção 4.2 ainda diz “quando o runtime estiver disponível”;
4. seção 5.3 afirma que a Figura 3 usa três vistas, mas a figura/caption usam quatro;
5. seção 5.4 afirma que a Figura 4 apresenta duas vistas, mas a versão atual apresenta uma;
6. a referência de Schönberger aparece como `Sch"onberger` no PDF e precisa de correção bibliográfica;
7. o texto de G3 deve deixar explícito que a diferença de poucos micrômetros é consistência numérica entre pose registrada e plano calculado, e não precisão física micrométrica do Gazebo.

## Melhoria visual recomendada antes do orientador

A Figura 5 já é uma comparação qualitativa válida entre referência, A0 e COLMAP, mas para um leitor não especialista deve ser mais autoexplicativa:
- usar subcaptions abaixo dos três painéis: “Referência”, “DM-NeRF A0”, “COLMAP”;
- manter rótulos fora da área dos dados;
- preferencialmente acrescentar uma segunda vista ou detalhe da mesma região para evidenciar espessamento/dispersão do COLMAP.

Isso é melhoria de comunicação, não nova execução experimental.

## O que deve ir para o branch work-codex-2026

Depois dessas correções:
- fonte LaTeX completo e figuras sob um diretório versionado de dissertação;
- PDF candidato ao orientador em `docs/exports/`;
- comando/documentação de compilação;
- atualização deste status.

Não versionar o bundle COLMAP completo, normal maps, depth maps ou `fused.ply` de 5,8 milhões de pontos. Para reprodutibilidade são suficientes o script, métricas JSON, parâmetros, proveniência e hashes dos artefatos externos.

Não alterar `master` ou `dissertacao-2026` durante esse fechamento.

## Mensagem sugerida ao orientador

Professor, encaminho uma versão atualizada da dissertação para revisão. Fechei o experimento principal com a reprodução do DM-NeRF, avaliação geométrica, comparação quantitativa e qualitativa com um baseline COLMAP na mesma cena, estruturação A0/A1/A2 e validação funcional no Gazebo. Mantive explícitas as limitações do estudo, principalmente o uso de uma única cena, a supervisão de instâncias, o bounding frame derivado da referência e o fato de o COLMAP ter recebido as poses.

Gostaria principalmente do seu retorno sobre três pontos: se o enquadramento da contribuição está adequado para a dissertação, se o nível de comparação com a literatura é suficiente e se o título/escopo estão formulados de forma correta. Depois desse retorno faço o fechamento editorial e institucional da versão de banca.
