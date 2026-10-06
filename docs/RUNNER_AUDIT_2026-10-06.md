# Auditoria e integração do executor — 06/10/2026

Base desta integração: `8727662b143cab09ffb0715a1524b7bf720f323e`.
AGENTS.md e todos os arquivos atuais de docs/ foram lidos antes das alterações. Decisões congeladas preservadas.

## Estado confirmado da branch

| Componente | Situação |
|---|---|
| Scripts legados sdf-transformer | Separação por cor e escrita OBJ/SDF presentes; paths absolutos, escala padrão zero e erros do multi_sdf_writer continuam documentados em TECHNICAL_FINDINGS.md |
| Arquivos históricos pc-files/results | Presentes, mas sem prova de origem suficiente para tratá-los como resultados desta execução |
| Piso e avaliação | tools/regularize_floor.py, evaluate_planarity.py e evaluate_mesh_distance.py já existem nesta revisão; sua presença não comprova ablation real concluída |
| Núcleo científico | Documentos novos reconhecem a supervisão 2D e o uso de GT no bounding frame; preservados |
| DM-NeRF | Código externo oficial, não incorporado ao legado; agora fixado em 4752087038c503cd608aa9dbd8861f3fc9259581 |
| Execução GPU | Preparada; ainda depende de ativação/execução na conta Kaggle/Colab |
| E0 completo / Gazebo | Não demonstrados por um smoke test de três passos |

## Problemas do runner anterior corrigidos

- `latest_run_dir` misturava o checkpoint do smoke com treino principal, embora smoke alterasse batch e amostras coarse/fine.
- O loop oficial avaliava dez vistas no passo zero mesmo com i_test alto.
- Não havia limite de tempo nem salvamento garantido ao encerrar a janela planejada.
- A retomada não preservava RNG Python/NumPy/Torch/CUDA.
- Clone usava HEAD móvel; download não validava checksum e extraía todas as cenas.
- O notebook exigia alterar RUN_FULL e usava comandos `!` cujo erro não interrompia necessariamente a sequência.
- Ambiente/dataset ficavam em /kaggle/working, misturados às saídas a preservar.

## Integração entregue

Novas ferramentas portáveis em tools/dmnerf, compatibilidade CLI em tools/kaggle_dmnerf.sh, notebook Kaggle existente atualizado e notebooks de continuação/Colab adicionados. Ferramentas científicas e scripts legados preservados.

Ambiente Python 3.10.16, Torch 2.2.2/CUDA 11.8, torchvision 0.17.2: adaptação explícita do ambiente oficial Python 3.7/Torch 1.8.1. Não afirmar equivalência numérica sem comparação. Dependências diretas fixadas; freeze efetivo é reutilizado na continuação e a identidade do experimento rejeita divergências.

A arquitetura, perdas, near/far, samples e schedule vêm da configuração oficial. Avaliação é separada do treino; isso também muda o consumo de RNG em comparação ao programa original. Smoke reduz dados, batch e grade, é diagnóstico e nunca alimenta o experimento.

## Limitação do meshing e contrato de instâncias

Mantidos os limites orientados pelo GT, extensões [1.9,7.0,7.0], ocupação 0.45 e limpeza de componentes menores que 400 triângulos. Densidade e grade são acumuladas em CPU, com consultas em lotes na GPU, para reduzir VRAM.

O `ins_map` de `objs_info_rigid.json` é fixo e não comprova o mapeamento de um novo treino. São exportados `instance_labels.npz` e `mesh_instances.ply` antes desse remapeamento. Não se inventam categorias semânticas nem se usa o semantic_classes.json histórico como GT atual. A seleção rastreável do piso permanece necessária antes de E2.

Sem superfície no limiar oficial, o executor grava `mesh_status.json`. No smoke isso é diagnóstico; em execução experimental bloqueia E0. Não reduz o limiar arbitrariamente para produzir uma malha.

## Continuidade e evidências

O ambiente temporário de 05/10 foi reiniciado antes da publicação dos commits locais. Seus logs/commits locais não estavam no GitHub e não foram recriados como se fossem originais. Esta integração parte da branch atual e registra novos testes em reports/2026-10-06-runner. Resultados anteriores observados na conversa não são apresentados como validação numérica da versão atual.

Impacto na dissertação: E0 passa a ter um executor com protocolo e proveniência explícitos; E3 ganha instrumentação real. Não significa que E0–E5 já estejam concluídos.
