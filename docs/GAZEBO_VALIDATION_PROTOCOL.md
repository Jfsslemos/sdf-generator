# Protocolo de validação funcional no Gazebo Classic

Este documento congela, antes de observar os artefatos finais, como A0/A1/A2 serão validados no simulador. O objetivo é medir **utilidade funcional para simulação**, e não transformar sucesso no Gazebo em evidência de fidelidade geométrica.

## Princípio

As métricas geométricas e de imagem permanecem independentes da validação funcional. Um artefato pode ser geometricamente próximo da referência e falhar como mundo de simulação, ou carregar corretamente no Gazebo e ainda apresentar erro geométrico relevante. Por isso não haverá score agregado entre essas famílias.

## Gates

### G0 — integridade do SDFormat
Aplicável a A0, A1 e A2.

PASS requer:
- XML/SDFormat parseável;
- nomes de modelos não vazios e únicos;
- referências de malha resolvíveis;
- escala de malha finita e estritamente positiva;
- pelo menos um `link` por modelo;
- elementos visual e collision esperados presentes.

G0 é validação estática e não prova funcionamento físico.

### G1 — carregamento no Gazebo Classic
Aplicável a A0, A1 e A2.

PASS requer que a cena abra no Gazebo Classic sem erro fatal relacionado ao SDF ou às malhas e permaneça carregada durante a inspeção inicial. Warnings devem ser preservados no log, mesmo quando o gate passar.

### G2 — individualização das instâncias
Primariamente A1 e A2.

Selecionar pelo menos três instâncias não-piso com IDs rastreáveis, quando existirem. Para cada uma, executar uma transformação independente conhecida (por exemplo, translação de 0,25 m em um único eixo) e verificar:
1. somente o modelo alvo muda de pose;
2. os demais modelos preservam suas poses;
3. a operação não exige editar a malha global.

PASS requer sucesso em todas as instâncias selecionadas. A seleção e os IDs devem ser registrados antes do teste. G2 é evidência funcional da separação explícita, não métrica semântica.

### G3 — piso e colisão
Exclusivo de A2 e **bloqueado até existir FLOOR_ID com proveniência rastreável**.

Após a regularização, registrar:
- `FLOOR_ID` e sua fonte;
- parâmetros usados por `regularize_floor.py`;
- relatório de planaridade antes/depois;
- resultado de um teste de apoio/contato no Gazebo.

PASS requer superfície de colisão utilizável para apoio no cenário de teste. O critério geométrico primário de A1→A2 continua sendo P95 do residual planar; G3 não o substitui.

### G4 — navegação curta
Exclusivo de A2 e condicionado à existência de uma configuração histórica reproduzível sem desenvolvimento relevante novo.

Executar uma trajetória curta, fixa e registrada entre poses livres. Registrar pose inicial, objetivo, planner/configuração e resultado.

Resultados possíveis:
- `PASS`: objetivo alcançado sem atravessar colisões da reconstrução;
- `FAIL`: execução válida, mas objetivo não alcançado ou colisão inválida;
- `NOT_EXECUTED`: teste exigiria implementação/configuração nova relevante.

`NOT_EXECUTED` não será convertido em PASS nem ocultado.

## Matriz pré-registrada

| Condição | G0 | G1 | G2 | G3 | G4 |
|---|---:|---:|---:|---:|---:|
| A0 — raw | obrigatório | obrigatório | não exigido | não exigido | não exigido |
| A1 — instâncias | obrigatório | obrigatório | obrigatório | não exigido | não exigido |
| A2 — instâncias+piso | obrigatório | obrigatório | obrigatório | obrigatório | condicionado |

## Evidência mínima por execução

Salvar um `gazebo_validation.json` contendo:
- `run_id`;
- condição `A0`, `A1` ou `A2`;
- commit do código;
- hash SHA-256 das malhas de entrada e do SDF;
- versão do Gazebo Classic;
- IDs de instância testados;
- `FLOOR_ID` e fonte, quando aplicável;
- resultado `PASS`/`FAIL`/`NOT_EXECUTED` por gate;
- caminhos para stdout/stderr e evidências;
- observações e warnings.

Screenshots podem complementar a evidência, mas não substituem logs e manifesto.

## Repetições e correções

Falha de integração pode ser corrigida e o gate repetido desde que a correção seja registrada e não altere silenciosamente a reconstrução avaliada. Se houver mudança na geometria, decomposição de instâncias ou regularização, o artefato recebe nova identidade/hash e a execução anterior permanece rastreável.

## Interpretação na dissertação

A validação no Gazebo responde se a reconstrução processada é utilizável como ativo de simulação nos testes definidos. Ela **não** demonstra, isoladamente, precisão geométrica, qualidade de síntese de vistas ou qualidade de segmentação. Essas propriedades permanecem cobertas pelas métricas específicas do protocolo experimental.

A dependência do meshing DM-NeRF da bounding frame obtida da referência DM-SR deve continuar declarada ao interpretar A0/A1/A2.
