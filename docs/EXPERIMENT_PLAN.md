# Plano experimental mínimo

## P0 — obrigatório

### E0 — Reproduzir DM-NeRF/DM-SR
Objetivo: executar pelo menos uma cena de DM-SR e recuperar as saídas necessárias ao pipeline.
Saídas: checkpoint, métricas oficiais, malha/outputs de instância e semântica, tempo de execução.

### E1 — Reproduzir o pós-processamento existente
Objetivo: transformar a saída de DM-NeRF em objetos separados e cena carregável no Gazebo.
Saídas: objetos independentes, comando reprodutível, cena funcional.

### E2 — Ablation do piso
Comparar a cena/mesh antes e depois da regularização do piso.
Métricas mínimas: residual ao plano (média/RMSE/P95) e efeito qualitativo/funcional no Gazebo.

### E3 — Custo computacional
Registrar tempo por etapa, GPU/VRAM quando disponível e tempo total.

### E4 — Avaliação funcional simples
Critérios binários/contáveis: carrega sem erro; objetos podem ser removidos/reposicionados separadamente; trajetória simples do robô é executável sem colisões espúrias atribuíveis ao piso.

## P1 — desejável

### E5 — Avaliação geométrica
Se houver GT 3D ou depth GT recuperável, medir precision/completeness/F-score em tolerâncias fixas e/ou Chamfer Distance.

### E6 — Baseline geométrico
COLMAP/OpenMVS somente se puder reutilizar as mesmas imagens/poses com setup controlado em <= 1 dia de engenharia.

### E7 — Baseline de decomposição
Preferir comparação oficialmente já definida no DM-NeRF ou um baseline pré-treinado de baixo custo; não treinar modelo novo sob pressão de prazo.

## P2 — opcional
- Replica como conjunto complementar;
- ScanNet;
- segundo baseline externo;
- qualquer migração de simulador.

## Regra de corte
Se P0 não estiver completo, nenhum item P2 pode consumir tempo.
