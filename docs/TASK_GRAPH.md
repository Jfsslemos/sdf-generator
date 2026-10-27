# Grafo de tarefas

P0.1 Recuperar DM-SR -> P0.2 Recriar ambiente DM-NeRF -> P0.3 Smoke test de treino/teste/meshing
                                                |
                                                v
                                         P0.4 Saídas reais
                                                |
              +---------------------------------+-------------------------------+
              |                                 |                               |
              v                                 v                               v
       E1 pós-processamento              E3 instrumentação              E5 geometria (se GT)
              |
              v
       E2 ablation piso
              |
              v
       E4 teste Gazebo

Baselines só entram após P0.3 e após confirmar formato/poses do dataset.

Texto pode avançar em paralelo em: introdução, fundamentação, relacionados, metodologia consolidada e reprodutibilidade. Resultados/discussão só devem receber números com origem rastreável.
