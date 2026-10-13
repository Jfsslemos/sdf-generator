# R92 — Perfil vertical exato de área em faces afetadas (13/10/2026)

Análise geométrica determinística de A0/A2/A2b da cena `study`, 710.928 faces correspondentes. O GT oficial `study.ply` (SHA256 `8de1c71689452af874d661b610873a036fddf979b89c86704e5537561c1452fc`) foi verificado como proveniência, mas **não foi usado na métrica**. Faces agrupadas por 0, 1, 2 ou 3 vértices deslocados A0→A2 acima de 1e-5 unidade. Área acima de cortes Y calculada exatamente por clipping baricêntrico; controle poligonal independente em 500 triângulos sintéticos, erro relativo máximo 1.6e-15.

| Área de faces afetadas | A0 | A2 | A2b (pós-hoc) |
|---|---:|---:|---:|
| Acima de Y=0.2 | 0.370327 | 10.929323 | 0.370327 |
| Acima de Y=0.5 | 0.171942 | 4.949247 | 0.171942 |
| Apenas faces com 1 vértice movido, acima de Y=0.2 | 0.280402 | 10.189541 | 0.280402 |

Os 101.988 vértices deslocados passam a ter Y<=0.050579 em A2, mas as faces parcialmente deslocadas permanecem ligadas a vértices elevados. Por isso, a área afetada acima de Y=0.2 cresce 29.51 vezes; 93.23% dessa área em A2 provém de faces com um único vértice deslocado. Não se trata de GT semântico de piso, escala física certificada, teste de colisão ou execução Gazebo. Não substitui o protocolo geométrico primário R71, no qual A2 piora globalmente. A2b é pós-hoc.

Artefatos locais: script `experimento_r92.py`, CSV/JSON, duas figuras, LaTeX institucional atualizado (67 páginas), manifesto de integridade e testes. Sem treinamento, COLMAP ou Gazebo.
