# Comparação crítica com métodos relacionados — 09/10/2026

> Documento de apoio ao capítulo de Trabalhos Relacionados. A comparação é **qualitativa e de literatura**: não reutiliza números publicados por outros trabalhos como se fossem resultados experimentais diretamente comparáveis aos da dissertação.

## Escopo da comparação

A banca de qualificação solicitou que a contribuição fosse contrastada de forma mais explícita com trabalhos existentes. Esta comparação separa três problemas que frequentemente aparecem misturados: (1) reconstrução/síntese e compreensão panóptica da cena; (2) obtenção de uma representação explícita e individualizável; e (3) geração de conteúdo utilizável em simulação robótica. Métodos diferentes cobrem subconjuntos distintos desses problemas e, por isso, não devem ser ordenados por um único critério.

A comparação de literatura também é distinta da comparação experimental. **A0/A1/A2 são uma ablação interna da cadeia proposta e não substituem um método externo.** O baseline COLMAP+dense MVS preparado no repositório, caso seja executado, será somente um termo de comparação geométrica: não fornece decomposição por instâncias, semântica nem integração com o simulador.

## Tabela comparativa

| Trabalho | Entrada principal | Representação / saída | Supervisão ou informação de instância/semântica | Geometria explícita | Individualização / edição estrutural | Destino de simulação | Limitação relevante para esta dissertação |
|---|---|---|---|---|---|---|---|
| **DM-NeRF** — Wang, Chen e Yang (2023) | imagens RGB, poses e máscaras 2D de instância no protocolo DM-SR | campo neural de radiância com decomposição por objeto; a geometria é obtida posteriormente por extração de malha | máscaras 2D de instância fornecidas ao treinamento | sim, por etapa posterior de extração | suporta decomposição/manipulação na representação neural, mas não entrega diretamente uma cena SDFormat organizada em modelos independentes | não é um pipeline completo de simulação | fornece o componente neural adotado aqui, mas não encerra a transformação em cena estruturada para Gazebo |
| **Panoptic Neural Fields** — Kundu et al. (2022) | imagens coloridas; poses, informação de objetos e segmentações 2D obtidas por métodos auxiliares | campo neural orientado a objetos, com representação separada de *things* e *stuff* | pseudo-supervisão a partir de predições 2D e informação de objetos | representação principal é neural/volumétrica | permite tarefas como edição 3D e reconstrução panóptica | não tem como objetivo produzir arquivo de cena robótica | enfatiza representação panóptica e edição, não a conversão rastreável para malhas de colisão e cena de simulador |
| **Panoptic Lifting** — Siddiqui et al. (2023) | imagens, poses e máscaras panópticas 2D produzidas por rede pré-treinada | campo neural panóptico 3D consistente entre vistas | máscaras panópticas 2D automáticas; associação linear trata inconsistência de IDs entre vistas | representação principal é um campo neural volumétrico | produz representação panóptica 3D consistente, não um conjunto de modelos de simulação independentes | não é o destino principal | resolve explicitamente a consistência panóptica multivista, mas não a etapa final de ativos de simulação |
| **PanoRecon** — Wu, Yan e Zha (2024) | vídeo monocular RGB | reconstrução panóptica 3D online/incremental, com geometria, semântica e instâncias | clustering de voxels e rastreamento/fusão de instâncias integram os fragmentos | sim, reconstrução 3D incremental | mantém instâncias coerentes entre fragmentos | não tem como objetivo principal gerar uma cena robótica com descrição de simulador | aproxima geometria e instâncias, mas encerra o problema na reconstrução/compreensão 3D |
| **URDFormer** — Chen et al. (2024) | imagem RGB e detecção/caixas de partes | URDF com estrutura articulada e ativos/meshes predefinidos | detector de partes + rede que prevê tipo de mesh, pose, escala e parentesco | sim, por composição de ativos | sim; estrutura articulada é parte central da saída | URDF carregável em simuladores e utilizado para treinamento robótico | depende da detecção; meshes predefinidas podem não corresponder à geometria observada; não prevê parâmetros como massa e atrito |
| **DRAWER** — Xia et al. (2025) | vídeo de cena interna estática | representação dual: SDF neural para geometria e Gaussian splats para aparência; módulo de articulação | modelos fundacionais apoiam inferência de articulações e partes | sim; geometria detalhada e formas simuláveis | sim, com articulações e partes interativas | compatível com game engines e plataformas de simulação robótica | objetivo real-to-sim mais amplo e protocolo diferente do DM-SR; não admite comparação quantitativa direta com os resultados desta dissertação |
| **GRS** — Zook et al. (2025) | uma observação RGB-D | compreensão da cena + associação com ativos prontos + geração de código/tarefas de simulação | SAM2/VLMs para segmentação e descrição; correspondência com ativos | não reconstrói primariamente a geometria observada; associa ativos prontos | objetos são representados por ativos preparados para simulação | geração explícita de simulações e tarefas robóticas | preservação geométrica da observação não é seu objetivo central; parte de RGB-D e de um conjunto de ativos disponíveis |
| **Cadeia desta dissertação** | DM-SR: RGB, poses e máscaras 2D de instância | DM-NeRF → malha explícita → objetos separados → regularização geométrica condicionada → SDFormat | decomposição supervisionada pelo protocolo DM-NeRF; piso selecionado por heurística geométrica, sem ground truth semântico | sim, extraída do campo neural | sim, por malhas individualizadas e modelos separados | Gazebo Classic via SDFormat | não infere física, articulações ou semântica do piso; estudo atual é restrito à cena *study* e ao protocolo DM-SR |

**Nota sobre GRS.** Esta tabela usa explicitamente o trabalho *GRS: Generating Robotic Simulation Tasks from Real-World Images*, de Zook et al. (CVPR Workshops 2025). A correspondência documental entre esse artigo e a sigla “GRS” usada no slide da qualificação deve ser conferida no material final, pois a apresentação não está versionada no repositório.

## Síntese crítica

**DM-NeRF, Panoptic Neural Fields e Panoptic Lifting** mostram formas diferentes de incorporar estrutura de objetos ou semântica a campos neurais. Eles são próximos do início da cadeia desta dissertação, mas não têm como objetivo final produzir uma coleção de malhas de colisão organizadas em uma cena robótica. No caso específico do DM-NeRF, a dissertação adota o método em vez de reivindicá-lo como contribuição própria. O avanço investigado está no que ocorre após a reconstrução neural: materialização da geometria, individualização conservadora, tratamento do piso, proveniência e validação no simulador.

**PanoRecon** aproxima-se mais da combinação entre reconstrução geométrica e organização panóptica. Sua proposta é reconstrução 3D panóptica online a partir de vídeo monocular, mantendo coerência entre fragmentos. Isso evidencia que reconstrução e instâncias podem ser resolvidas conjuntamente sem que a saída seja, necessariamente, uma cena de simulação. A comparação com PanoRecon é, portanto, conceitual: o destino e o protocolo experimental diferem.

**URDFormer, DRAWER e GRS** aproximam-se do problema de real-to-sim. URDFormer prevê diretamente URDFs com estrutura articulada a partir de imagens, mas utiliza tipos de mesh predefinidos e reconhece dependência do detector e ausência de parâmetros físicos como massa e atrito. DRAWER busca um ambiente fotorealista e interativo, com geometria detalhada e articulações, combinando SDF e Gaussian splatting. GRS parte de uma observação RGB-D e associa elementos detectados a ativos já preparados para simulação, além de gerar tarefas e código de simulação. Esses trabalhos mostram que “gerar uma cena simulável” pode significar reconstruir a geometria observada, compor ativos estruturados ou combinar estratégias.

A cadeia desta dissertação ocupa um ponto específico nesse espaço. Ela **preserva como ponto de partida a geometria reconstruída pelo DM-NeRF** e transforma essa geometria em entidades explícitas antes de aplicar uma regularização geométrica limitada ao piso. Não há recuperação de ativos CAD, previsão de articulações ou inferência de propriedades físicas. A contribuição defendida, portanto, não é a cobertura mais ampla do problema real-to-sim nem superioridade sobre esses sistemas; é a **avaliação rastreável da transição de uma reconstrução neural decomposta para uma cena explícita, individualizável e testável no Gazebo Classic**, mantendo separadas as evidências de síntese, decomposição, geometria, pós-processamento e funcionamento no simulador.

Essa formulação explicita também uma limitação. Enquanto URDFormer, DRAWER e GRS tratam interatividade, articulação ou geração de tarefas de forma mais direta, a cena produzida aqui não recupera dinâmica, massa, atrito ou articulações. Em contrapartida, GRS e URDFormer dependem de ativos disponíveis/predefinidos, enquanto a cadeia atual busca conservar a geometria observada até o pós-processamento. Essas diferenças são de escopo e representação, não uma demonstração de superioridade.

## Comparação de literatura versus comparação experimental

A tabela acima responde à exigência de posicionamento científico perante a literatura. Ela **não é uma avaliação experimental comum**, porque os trabalhos usam entradas, datasets, métricas e objetivos distintos.

A comparação experimental planejada é mais restrita:

- **A0/A1/A2:** ablação interna da cadeia; mede o efeito da individualização e da regularização do piso somente nas propriedades que essas etapas podem alterar.
- **COLMAP + dense MVS:** candidato a baseline geométrico externo, usando a cena *study*, as poses/intrínsecos conhecidos e a mesma avaliação geométrica. Se executado, compara apenas geometria.
- **Métodos da tabela:** não terão seus números publicados transplantados para as tabelas experimentais da dissertação. Comparações quantitativas diretas só seriam válidas sob protocolo compatível, o que não está estabelecido aqui.

## Referências verificadas usadas nesta comparação

- KUNDU, A. et al. *Panoptic Neural Fields: A Semantic Object-Aware Neural Scene Representation*. CVPR, 2022.
- SIDDIQUI, Y. et al. *Panoptic Lifting for 3D Scene Understanding With Neural Fields*. CVPR, 2023, p. 9043–9052.
- WU, D.; YAN, Z.; ZHA, H. *PanoRecon: Real-Time Panoptic 3D Reconstruction from Monocular Video*. CVPR, 2024, p. 21507–21518.
- CHEN, Z. Q. et al. *URDFormer: A Pipeline for Constructing Articulated Simulation Environments from Real-World Images*. Robotics: Science and Systems, 2024. DOI: 10.15607/RSS.2024.XX.124.
- XIA, H. et al. *DRAWER: Digital Reconstruction and Articulation With Environment Realism*. CVPR, 2025, p. 21771–21782.
- ZOOK, A. et al. *GRS: Generating Robotic Simulation Tasks from Real-World Images*. CVPR Workshops, 2025, p. 594–603.
- WANG, B.; CHEN, L.; YANG, B. *DM-NeRF: 3D Scene Geometry Decomposition and Manipulation from 2D Images*. ICLR, 2023.
