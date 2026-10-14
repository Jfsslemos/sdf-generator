# R108 — controle exploratório de suavização de Taubin (14/10/2026)

**Escopo:** experimento geométrico real sobre A0 da cena DM-SR Study. Controle **T** pós-hoc, não condição primária nem baseline neural. A0, A2 e GT oficial verificados por SHA-256; GT usado somente na avaliação.

**Procedimento:** Taubin com Laplaciano uniforme, dez passadas alternando +0,50 e -0,53; 3.918 vértices de borda fixos; 710.928 faces preservadas. Sem ajuste de parâmetros por busca no GT. Avaliação suplementar: 200.000 pontos/superfície, sementes 42/43/44, vizinho ponto-ponto bilateral, tolerâncias 0,01/0,02/0,05 unidade do dataset.

| Condição | Distância bidir. | F@0,01 | F@0,02 | F@0,05 |
|---|---:|---:|---:|---:|
| A0 | 0,084638 | 0,048480 | 0,197759 | 0,775073 |
| A2 | 0,088567 | 0,038830 | 0,165172 | 0,758320 |
| T | 0,084244 | 0,048340 | 0,197626 | 0,777170 |

T reduziu ligeiramente a distância média e elevou F@0,05, mas não melhorou uniformemente os F-scores. A2 permaneceu inferior nas médias mostradas. Não há significância estatística entre cenas: são reamostragens de uma única cena. Escala física não certificada. A soma das médias é suplementar e **não substitui R71**, cujo resultado primário segue desfavorável a A2.

**Referência:** Taubin, *A Signal Processing Approach to Fair Surface Design*, SIGGRAPH 1995, DOI 10.1145/218380.218473.

**Estado funcional:** G2 incompleto, G3 pontual, G4 não executado; COLMAP não executado. Nenhum resultado funcional novo.

**Integração:** seção nova 5.9, tabela, duas figuras e ressalvas na discussão/limitações da versão LaTeX R106; pacote local R108 com script, PLY T, CSV/JSON, PDF e hashes. A publicação desta nota não significa sincronização do manuscrito institucional.