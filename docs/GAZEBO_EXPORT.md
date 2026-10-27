# Exportação rastreável para Gazebo Classic

`tools/export_gazebo_scene.py` implementa o caminho novo, preservando o código
legado. Recebe `mesh_geometry.ply` e `instance_labels.npz` da mesma extração.
Valida correspondência de vértices e topologia. A2 admite deslocamento de
vértices, mas exige a mesma topologia/ordem e um JSON de proveniência do piso.
Cores não são utilizadas para atribuir IDs ou classes.

```bash
python tools/export_gazebo_scene.py mesh_geometry.ply instance_labels.npz results/gazebo_a0 --condition A0 --up-axis y
python tools/export_gazebo_scene.py mesh_geometry.ply instance_labels.npz results/gazebo_a1 --condition A1 --up-axis y
python tools/export_gazebo_scene.py results/a2_regularized.ply instance_labels.npz results/gazebo_a2 --condition A2 --up-axis y --floor-provenance results/floor_selection.json
```

Os exemplos `--up-axis y` são condicionais: confirmar a convenção do artefato
na proveniência; se a regularização alinhou a cena a z, usar `--up-axis z`.
O argumento é obrigatório para impedir uma suposição silenciosa. Uma rotação
rígida comum leva o eixo vertical indicado a +Z do Gazebo. A rotação fica na
pose de cada modelo, não altera as malhas usadas nas métricas, nem a escala.
Os objetos mantêm a origem comum da cena: modificar a pose de um modelo
translada apenas sua geometria; rotações ocorrem ao redor dessa origem comum.

Saídas: `scene.world`, `meshes/*.obj`, `meshes/*.ply`, `meshes/instances.json`,
`manifest.json`, `gazebo_validation.json` e `export.log`. Modelos
`instance_NNN` são estáticos,
com link, visual e collision independentes; A0 tem um único `scene_raw`.
URIs são relativas ao world e `scale=1 1 1`. Copiar o diretório completo
preserva referências. Não há dependência de paths pessoais, Fuel, sun ou
modelos externos. O diretório de saída precisa estar vazio para não sobrescrever
evidências anteriores. Arquivos e JSON de proveniência têm hashes SHA-256.

A0 conserva todas as faces. A1/A2 seguem a regra registrada da separação:
somente faces com três IDs iguais são atribuídas. Faces de fronteira omitidas
são contadas, com warning explícito; a perda de cobertura pode criar aberturas.
A geometria visual e a geometria de colisão são a mesma malha triangular, sem
simplificação silenciosa. Malhas não estanques geram warning: colisão utilizável
não é garantida por XML válido.

A exportação executa apenas G0 (parser XML da biblioteca padrão, nomes,
links, visual/collision, escalas e referências locais). Esse gate é uma
validação estrutural do subconjunto gerado, não uma validação completa do
schema SDFormat. Não executa o parser nativo libsdformat nem
Gazebo. G1–G4 permanecem `NOT_EXECUTED`, versão Gazebo é null e IDs testados
em runtime são uma lista vazia. G3 continua condicionado ao piso rastreável e
a teste de apoio real. O JSON de proveniência é preservado como evidência,
não convertido em alegação de ground truth. O exportador não resolve por si
só a identificação semântica do piso.

Testes CPU: `python -m unittest discover -s tests -p test_gazebo_scene.py -v`.
Usam malhas sintéticas para comparar A0/A1/A2, realocação do pacote, IDs
repetidos/grandes, rejeição de IDs negativos, geometria incompatível, XML
malformado, nomes duplicados, escala inválida, mesh ausente e divergência entre
visual/collision. Artefatos finais da reconstrução ainda são necessários para
a validação da cena científica.

## Auditoria do legado

Os scripts em `sdf-transformer/scripts/` permanecem inalterados apenas para
rastreabilidade. Eles não devem ser usados no novo caminho: contêm paths
`/home/joao`, usam RGB como separador, criam diretórios durante o loop, misturam
origens de URI, escrevem escala zero e, no writer múltiplo, referenciam variáveis
não definidas. O exportador novo deriva os nomes exclusivamente do inteiro
`instance_id`; isso identifica instâncias, não atribui semântica a nenhum ID.
