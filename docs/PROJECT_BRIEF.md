# Project Brief — Dissertação

## Tema
Reconstrução semântica automatizada de ambientes domésticos para simulação robótica.

## Núcleo técnico mantido
No protocolo DM-SR efetivamente suportado pelo DM-NeRF, a entrada de treinamento inclui imagens RGB posicionadas **e supervisão 2D de instâncias fornecida pelo conjunto de dados**. A cadeia mantida é:

RGB + poses + máscaras de instância 2D -> DM-NeRF -> reconstrução/malha com informação de instância -> separação de elementos -> pós-processamento geométrico (incluindo piso) -> cena carregável no Gazebo.

A dissertação não deve afirmar automação ponta a ponta a partir apenas de RGB enquanto essa supervisão 2D vier do dataset. Esse ponto deve aparecer explicitamente nas limitações e na descrição experimental.

## Mudança após a qualificação
A dissertação não mudará para um novo pipeline baseado em Nerfacto/OneFormer nem terá recuperação CAD como extensão obrigatória. O avanço em relação ao TCC será obtido principalmente por:
- avaliação mais rigorosa;
- comparação com baselines viáveis;
- ablations do pós-processamento;
- análise de limitações;
- reprodutibilidade;
- texto e discussão em nível de mestrado.

## Pergunta de pesquisa provisória
Em que medida uma reconstrução neural com decomposição de instâncias, combinada a pós-processamento geométrico, permite gerar ambientes domésticos estruturados para simulação robótica?

## Hipótese de trabalho provisória
A decomposição de instâncias fornecida pelo DM-NeRF, combinada à separação dos elementos e à regularização geométrica, permite transformar a reconstrução em uma cena estruturada para simulação; a adequação deve ser demonstrada por critérios visuais, geométricos, estruturais, funcionais e computacionais, e não apenas por métricas de síntese de vistas.

## Escopo negativo
- sem nova arquitetura neural;
- sem OneFormer como método principal;
- sem Nerfacto como substituição metodológica;
- sem CAD retrieval no caminho crítico;
- sem inferência de massa/inércia/articulações;
- sem migração de Gazebo por motivação puramente tecnológica;
- sem alegar entrada exclusivamente RGB quando o protocolo executado usa máscaras 2D de instância.
