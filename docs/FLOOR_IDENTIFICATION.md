# Identificação rastreável do piso — DM-SR study

## Conclusão da inspeção oficial

**Não há semântica oficial suficiente, nos artefatos inspecionados, para atribuir um ID específico ao piso.** Isso não exclui a existência de metadados não publicados pelos autores. Nenhum ID foi declarado ground truth semântico do piso.

Inspeção reproduzida em 07/10/2026 no ZIP oficial SHA-256 `146ddd88d34cf8efc3357737871325f2ad1fe7584f7e20fc8ec75f5d3baed602` e upstream `4752087038c503cd608aa9dbd8861f3fc9259581`. O script verifica todos os 2414 arquivos de study contra o arquivo ZIP validado. Relatório: `reports/2026-10-07-floor/official-audit.json`.

| Artefato | Evidência efetivamente encontrada |
|---|---|
| transforms train/test/mani | poses, paths das imagens, camera_angle_x e rotation quando presente; sem classe semântica |
| 300 máscaras train + 100 test, 400×400 | IDs inteiros 0–12; histogramas por ID registrados, sem nomes de classes |
| ins_rgb.hdf5 | um dataset `datasets`, int16, 13×3; paleta de cores; nenhum atributo semântico |
| objs_info_rigid.json | table_3 → obj_gt_id 10; chair_2 → obj_gt_id 8; nenhum objeto nomeado floor |
| objs_info_deform.json | table_3 e parâmetros de manipulação; nenhum piso |
| transformation_matrix.json | transformações de demonstrações, sem catálogo semântico |
| upstream data/color_dict.json | study contém mapeamento identidade de 0–12 para índices de paleta, sem classes |
| study.ply | 437008 vértices e 844701 faces; propriedades x/y/z e vertex_indices, sem cor, instance_id ou classe |
| ins_map | correspondência de IDs do exemplo fornecido; não identifica classe piso e não pode ser transferida automaticamente para um treino novo |

O avaliador upstream recalcula associações de instâncias por vista (`networks/tester.py`). Os canais preditos não possuem identidade semântica fixa garantida entre treinos. Frequência de pixels, cor e o arquivo histórico `semantic_classes.json` não foram usados para declarar piso.

## Heurística geométrica, não ground truth

`tools/select_floor.py` recebe **mesh_geometry.ply + instance_labels.npz**. Verifica vértices, coordenadas, ordem, índices e topologia antes de associar IDs. Cores não entram na decisão. A saída inclui hashes de ambos os inputs, parâmetros, diagnósticos e score por instância, `semantic_ground_truth=false` e `evidence_type=geometric_heuristic`.

Regra v2, definida antes de observar a mesh final:

1. Considerar somente faces cujos três vértices têm o mesmo ID. Faces de área zero não contribuem; IDs sem faces válidas recebem rejeição explícita.
2. Ajustar plano por covariância dos vértices das faces, ponderados pela área dos triângulos. Registrar normal, altura do centro ponderado, RMSE e área.
3. Aceitar como candidato apenas área ≥0,5 m², pelo menos 85% da área com normal até 15° da vertical (em módulo), normal do plano até 15°, RMSE ≤0,03 m e altura até o percentil 1 dos vértices da cena +20% da amplitude vertical.
4. Entre candidatos, score = área total. Escolher a maior área. Se a segunda área for ≥80% da primeira, retornar `ambiguous` e ID null. Sem candidato, retornar `not_identified` e ID null. Não usar o número do ID para desempatar semanticamente.

A vertical padrão é **+Y no referencial da mesh exportada/GT**, com unidades métricas assumidas do dataset. O código oficial consulta a rede transformando `[x,y,z]` da mesh para `[x,-z,y]`; as poses da rede estão em outro referencial. Não usar +Z das poses diretamente na mesh. `--up` registra uma alternativa explícita para outras convenções; não é estimativa automática de gravidade.

Limitações: um tapete/plataforma baixo pode vencer; piso fragmentado em vários IDs ou fundido com paredes pode ser recusado; faces de fronteira ficam fora das áreas; outliers e malhas incompletas podem alterar o limite de altura. A regra identifica um **candidato geométrico** e não demonstra sua classe. Alterações futuras dos limiares exigem nova versão e registro, sem ajustar silenciosamente após observar a ablation. O residual usado para seleção não comprova melhora de reconstrução.

## Execução reproduzível

Dependências CPU: numpy, trimesh; auditoria adicional: pillow, h5py. Ambiente efetivamente usado no relatório `environment.json`.

```bash
python tools/audit_dmsr_floor.py /tmp/dmsr-floor/dmsr/study \
  --archive /tmp/dmsr-floor/dmsr.zip --upstream /tmp/floor-upstream \
  --out reports/2026-10-07-floor/official-audit.json

python tools/select_floor.py instance_labels.npz --mesh mesh_geometry.ply \
  --out floor_selection.json

python -m unittest discover -s tests -p test_floor_selection.py -v
```

A saída não modifica malha, labels, checkpoint ou protocolo de treino. A2 só pode prosseguir quando `status=selected`, mantendo no relatório a natureza heurística da seleção e o hash dos inputs; `ambiguous` e `not_identified` mantêm o gate bloqueado. Nenhum ID da execução final foi escolhido nesta sessão: a mesh/labels finais ainda não estão disponíveis.

Impacto na dissertação: torna a seleção do piso reproduzível e auditável, distinguindo supervisão de instâncias, semântica oficial ausente e hipótese geométrica usada na ablation.
