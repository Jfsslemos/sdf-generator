# Plano experimental mínimo

## P0 — obrigatório

### E0 — Reproduzir DM-NeRF/DM-SR
Objetivo: executar pelo menos a cena `study` do DM-SR e recuperar as saídas necessárias ao pipeline.
Entrada documentada: RGB + poses + mapas 2D de instância fornecidos pelo DM-SR.
Saídas: checkpoint, métricas oficiais, malha com instâncias, tempo de execução e ambiente registrado.

### E1 — Reproduzir o pós-processamento existente
Objetivo: transformar a saída de DM-NeRF em objetos separados e cena carregável no Gazebo.
Saídas: objetos independentes, comando reprodutível, cena funcional.

### E2 — Ablation do piso
Comparar a mesma reconstrução antes e depois da regularização do piso.
Métricas mínimas: distância dos vértices de piso ao plano estimado (média, RMSE e P95), fração de inliers do RANSAC e efeito funcional/qualitativo no Gazebo.
A seleção da classe/cor do piso deve ser rastreável ao dataset; não inferir pela aparência da mesh.

### E3 — Custo computacional
Registrar tempo por etapa, modelo de GPU, VRAM quando disponível e tempo total. Não reutilizar a estimativa oral de ~3 h como dado experimental.

### E4 — Avaliação funcional simples
Critérios objetivos: parsing/carregamento sem erro; entidades separadas podem ser removidas/reposicionadas individualmente; e, se o teste de navegação já existente puder ser reproduzido sem grande implementação, completar uma trajetória simples sem colisões espúrias atribuíveis ao piso.

### E5 — Comparação interna obrigatória
Usar as etapas do próprio pipeline como termos de comparação:
- C0: malha/saída de DM-NeRF antes do pós-processamento;
- C1: saída com separação de instâncias;
- C2: saída com separação + regularização do piso.
Não condensar tudo em uma única pontuação: cada etapa deve ser avaliada somente nas propriedades que pode alterar.

## P1 — desejável

### E6 — Avaliação geométrica
O DM-SR possui uma malha de referência por cena usada pelo modo oficial de meshing. Medir Precision, Completeness, F-score e distância simétrica/Chamfer com amostragem de superfície.

**Cuidado metodológico:** a implementação oficial de `tools/mesh_generator.py` usa a malha de referência para obter o bounding frame da grade de extração. Portanto, o GT não é completamente independente da geração da malha prevista. Essa dependência deve ser declarada. Se houver tempo, repetir a extração com limites derivados apenas das câmeras/reconstrução; caso contrário, tratar as métricas geométricas como avaliação dentro do protocolo oficial, com essa limitação explícita.

Tolerâncias candidatas: 1 cm, 2 cm e 5 cm. A escolha final deve ser justificada no texto e permanecer fixa para os resultados finais.

### E7 — Baseline externo
Executar **no máximo um** baseline externo se o setup total ficar abaixo de um dia de engenharia. COLMAP/OpenMVS é candidato para geometria, mas não é obrigatório se ameaçar P0. A dissertação não deve sacrificar a avaliação do pós-processamento para reproduzir vários reconstrutores.

### E8 — Comparação de decomposição
Usar primeiro as métricas já implementadas pelo DM-NeRF: AP em IoU 0.50, 0.75, 0.80, 0.85, 0.90 e 0.95. Um baseline de segmentação/decomposição externo só entra se estiver disponível pré-treinado e não exigir novo treinamento.

## P2 — opcional
- Replica como conjunto complementar;
- ScanNet;
- segundo baseline externo;
- cena real;
- qualquer migração de simulador.

## Regra de corte
Se E0–E5 não estiverem completos e documentados, nenhum item P2 pode consumir tempo. Um baseline externo que não estiver operacional em um dia é cortado.
