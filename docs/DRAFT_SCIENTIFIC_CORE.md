# Rascunho — núcleo científico após auditoria do DM-NeRF

> Este arquivo é um rascunho para discussão. Não substitui automaticamente o texto da dissertação.

## Problema corrigido
A versão de qualificação descrevia uma cadeia futura com ScanNet, Nerfacto, OneFormer, associação multivista própria e recuperação CAD. Essa cadeia não será implementada. A execução final deve refletir o método realmente usado: DM-NeRF no DM-SR, seguido do pós-processamento que individualiza elementos e prepara a cena para o simulador.

A auditoria do código oficial do DM-NeRF também mostra que o treinamento no DM-SR recebe máscaras 2D de instância como supervisão. Por isso, a formulação final não deve sugerir que toda a estrutura semântica é inferida somente a partir das imagens RGB.

## Pergunta recomendada
**Em que medida uma reconstrução neural com decomposição de instâncias, combinada a pós-processamento geométrico, permite gerar ambientes domésticos estruturados para simulação robótica?**

Vantagens:
- descreve o que efetivamente será executado;
- não transforma SDFormat em contribuição;
- não promete segmentação automática ausente do protocolo;
- permite responder quantitativamente com reconstrução, decomposição, pós-processamento e teste funcional.

## Objetivo geral recomendado
**Avaliar a capacidade de uma cadeia baseada em DM-NeRF e pós-processamento geométrico de transformar reconstruções neuralmente decompostas em ambientes domésticos estruturados para simulação robótica.**

## Objetivos específicos recomendados
1. Reproduzir e documentar a reconstrução e decomposição de cenas do DM-SR com DM-NeRF.
2. Quantificar a fidelidade visual e a qualidade da decomposição usando as métricas suportadas pelo método e pelo conjunto de dados.
3. Avaliar a qualidade geométrica das reconstruções quando houver referência tridimensional apropriada, separando essa análise das métricas de síntese de vistas.
4. Avaliar o efeito da separação de elementos e da regularização do piso por meio de ablations controladas.
5. Verificar a geração de uma cena estruturada no Gazebo por critérios funcionais simples e reproduzíveis.
6. Medir o custo computacional das principais etapas e documentar o procedimento necessário para reproduzir os experimentos.
7. Comparar o método com ao menos um termo de comparação tecnicamente viável, externo ou interno, sem comprometer o caminho crítico da dissertação.

## Contribuição a defender
A contribuição não é o formato SDFormat nem uma nova arquitetura neural. O trabalho investiga e avalia a passagem de uma reconstrução neural decomposta para uma representação explícita e estruturada de ambiente destinada à simulação robótica. O ganho em relação ao TCC deve aparecer principalmente na avaliação sistemática, nas ablations, na análise de limitações e na reprodutibilidade.

## Limitações que devem ser assumidas
- o protocolo DM-SR do DM-NeRF usa supervisão 2D de instâncias;
- o cenário é estático;
- propriedades físicas não observáveis, como massa, atrito e articulações, não são inferidas;
- a regularização do piso pressupõe uma superfície predominantemente plana;
- a extração de mesh oficial do DM-NeRF usa a malha de referência para definir o volume/orientação de consulta; qualquer avaliação geométrica baseada nessa saída deve declarar essa dependência;
- cenas ou objetos pouco amostrados podem apresentar perda de geometria.
