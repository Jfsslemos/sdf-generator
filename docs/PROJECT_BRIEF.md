# Project Brief — Dissertação

## Tema
Reconstrução semântica automatizada de ambientes domésticos para simulação robótica.

## Núcleo técnico mantido
Imagens posicionadas -> DM-NeRF -> representação/malha com informação de instância/semântica -> separação de elementos -> pós-processamento geométrico (incluindo piso) -> cena carregável no Gazebo.

## Mudança após a qualificação
A dissertação não mudará para um novo pipeline baseado em Nerfacto/OneFormer nem terá recuperação CAD como extensão obrigatória. O avanço em relação ao TCC será obtido principalmente por:
- avaliação mais rigorosa;
- comparação com baselines viáveis;
- ablations do pós-processamento;
- análise de limitações;
- reprodutibilidade;
- texto e discussão em nível de mestrado.

## Pergunta de pesquisa provisória
Em que medida a reconstrução neural com decomposição de objetos pode automatizar a geração de ambientes domésticos estruturados para simulação robótica?

## Hipótese de trabalho provisória
A decomposição de objetos fornecida pelo DM-NeRF, combinada ao pós-processamento geométrico, permite gerar cenas estruturadas úteis para simulação, mas sua adequação precisa ser medida por critérios além da fidelidade de novas vistas.

## Escopo negativo
- sem nova arquitetura neural;
- sem OneFormer como método principal;
- sem Nerfacto como substituição metodológica;
- sem CAD retrieval no caminho crítico;
- sem inferência de massa/inércia/articulações;
- sem migração de Gazebo por motivação puramente tecnológica.
