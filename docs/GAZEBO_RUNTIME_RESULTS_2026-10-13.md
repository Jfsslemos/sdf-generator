# Validação funcional no Gazebo Classic — 13/10/2026

## Ambiente

Execução realizada no Gazebo Classic 11.10.2 a partir do pacote gerado para A0/A1/A2.

## G1 — carregamento

PASS para A0, A1 e A2.

Nos três casos, `gzserver` carregou o mundo e permaneceu ativo durante a janela de verificação. Os logs registram avisos de material ausente nos OBJ, mas nenhum erro fatal associado aos modelos.

## G2 — manipulação independente

PASS para A1.

A instância `instance_006` foi endereçada diretamente. Antes do comando, a posição registrada era `0 0 0`; após o deslocamento, a coordenada x passou para `0.25`. A operação foi dirigida somente a esse modelo.

## G3 — apoio/colisão do piso A2

PASS após auditoria do script e dos logs.

O arquivo `scene_g3_probe.world` define a caixa dinâmica `g3_probe` com:
- lado: 0,1 m;
- massa: 0,2 kg;
- centro inicial: `z=0.65 m`.

O helper `start_server` aguarda 6 s antes de retornar. Portanto, a pose denominada `initial` em `g3_pose.txt` já foi medida depois da queda e do assentamento da caixa:
- primeira pose medida após o carregamento: `z=0.093811 m`;
- pose após mais 8 s: `z=0.093806 m`;
- variação: aproximadamente 5 micrômetros.

A face inferior da caixa nessa pose está em `z=0.043806 m`. O plano regularizado da instância 10, após a rotação de +Y para +Z usada na exportação ao Gazebo, prevê no ponto final `(x,y)=(3.07411,-3.31338) m` uma altura de aproximadamente `z=0.043810 m`. A diferença é inferior a 4 micrômetros.

Assim, a caixa caiu aproximadamente 0,56 m, foi interrompida pela superfície regularizada e permaneceu estável durante a segunda janela de observação.

A linha automática `G3 A2: INCONCLUSIVO` do script original é um falso inconclusivo: a lógica comparava duas poses já posteriores ao assentamento. Não houve evidência de atravessamento do piso.

A captura de tela fornecida pelo autor também mostra o corpo dinâmico vermelho apoiado sobre a cena A2.

## Limite da evidência

G3 verifica contato em um ponto da superfície. As malhas exportadas não são estanques; portanto, o resultado não demonstra ausência de falhas de colisão em toda a malha.

G4 (navegação) permanece não executado e opcional segundo o protocolo congelado.
