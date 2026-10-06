# Rascunho — Metodologia científica executada

> Texto de trabalho para integração posterior à dissertação. Não contém resultados do smoke ou do piloto.

## Delineamento

O estudo será conduzido como uma avaliação experimental de uma cadeia de reconstrução e estruturação de cenas domésticas. O DM-NeRF, executado sobre o conjunto DM-SR, constitui o componente neural principal. A saída reconstruída é submetida a etapas de extração e pós-processamento geométrico até a obtenção de uma representação explícita composta por elementos individualizáveis e adequada à descrição de uma cena no Gazebo Classic. O SDFormat é tratado somente como mecanismo de integração com o simulador, e não como contribuição científica.

A análise separa três tipos de evidência: qualidade de síntese/decomposição fornecida pelo protocolo oficial do DM-NeRF; qualidade geométrica da representação explícita; e efeito das transformações introduzidas pelo pós-processamento. Essa separação evita inferir qualidade geométrica apenas a partir de métricas de renderização.

## Entradas e supervisão

Para cada cena, o treinamento do DM-NeRF utiliza imagens RGB, poses de câmera e mapas bidimensionais de instância, incluindo os dados de instância disponibilizados pelo DM-SR. Portanto, a decomposição avaliada não deve ser descrita como obtida exclusivamente a partir de RGB. Os experimentos preservarão a configuração oficial sempre que tecnicamente compatível com o ambiente de execução, registrando qualquer adaptação necessária para reprodução.

## Condições experimentais

São definidas três condições encadeadas. **C0** corresponde à geometria extraída do modelo neural antes das transformações geométricas propostas neste trabalho. **C1** corresponde à representação após a individualização/estruturação dos elementos da cena. **C2** acrescenta a regularização geométrica do piso sobre C1. C0 é a referência interna para caracterizar a geometria produzida pelo estágio neural; C1 isola o efeito da estruturação; e C2 permite medir especificamente o efeito da regularização do piso.

As condições derivadas de uma mesma reconstrução devem compartilhar o mesmo identificador de execução e os mesmos artefatos de origem. Ajustes manuais posteriores à observação de um resultado exigem novo identificador, de modo que tentativas malsucedidas não sejam silenciosamente substituídas.

## Métricas

A reprodução do DM-NeRF utilizará o avaliador oficial para PSNR, SSIM e LPIPS na síntese de vistas e Average Precision de instâncias nos limiares de IoU 0,50, 0,75, 0,80, 0,85, 0,90 e 0,95. Essas métricas caracterizam o componente neural e não serão apresentadas como evidência direta de correção geométrica.

Quando houver referência tridimensional apropriada, a avaliação geométrica reportará distâncias direcionais entre superfícies, distância simétrica e medidas de precisão/completude ou F-score nos limiares definidos pelo protocolo experimental. Para o piso, C1 e C2 serão comparados de forma pareada por cena usando erro absoluto médio, RMSE, percentil 95 da distância ao plano e proporção de inliers. A cena, e não cada vértice, é a unidade experimental.

O percentil 95 é a medida primária da ablation C1→C2. Serão apresentados os valores de C1, C2 e a diferença por cena, além da mediana da diferença, intervalo interquartil e contagem de cenas com melhora, empate ou piora. Testes inferenciais somente serão utilizados caso haja número suficiente de cenas independentes; vértices de uma mesma malha não serão tratados como replicações independentes.

## Restrição da avaliação geométrica

O procedimento oficial de meshing do DM-NeRF para DM-SR carrega a malha de referência `<scene>.ply` e utiliza sua oriented bounding box para definir o volume e o referencial espacial em que o campo neural é consultado. Consequentemente, uma comparação posterior entre a malha extraída dessa forma e a mesma referência tridimensional não é totalmente independente: a referência não fornece os valores de densidade do campo, mas participa da definição do domínio de extração. Os resultados geométricos obtidos sob esse procedimento serão apresentados com essa dependência explicitamente declarada e não serão interpretados como avaliação de um pipeline que desconhece integralmente a geometria de referência.

## Integração no simulador

A validação no Gazebo Classic será funcional. A representação deverá ser carregável como cena, preservar a presença das entidades esperadas, permitir manipulação e remoção independente de elementos e oferecer uma superfície de suporte válida no teste definido para o piso. Essa avaliação demonstra integração da representação no cenário ensaiado; não demonstra equivalência física com o ambiente real. Massa, atrito, inércia, articulações e outras propriedades não observadas não são inferidas pelo método.

## Custo computacional e reprodutibilidade

Tempo de execução, throughput e uso de memória da GPU serão registrados nas etapas principais. O treinamento principal será executado apenas em recursos gratuitos, priorizando Kaggle e utilizando Colab Free como contingência. Smoke tests e pilotos destinam-se exclusivamente à validação da infraestrutura e ao planejamento do experimento; seus checkpoints e métricas não serão incorporados aos resultados científicos.

Cada resultado deverá manter rastreabilidade para cena, configuração, revisão do código, ambiente de execução e artefatos de origem. Resultados históricos sem proveniência suficiente serão identificados como históricos e não serão apresentados como reproduções atuais.

## Ameaças à validade

As principais ameaças previstas são a dependência da referência tridimensional na definição do volume de meshing; a supervisão por mapas 2D de instância; a quantidade e diversidade limitadas de cenas; a hipótese de planaridade usada na regularização do piso; e a ausência de inferência de propriedades físicas. Além disso, diferenças de ambiente de software podem exigir correções de compatibilidade no código original. Essas correções devem ser restritas à execução e avaliação, documentadas e separadas de alterações que modifiquem o método científico.
