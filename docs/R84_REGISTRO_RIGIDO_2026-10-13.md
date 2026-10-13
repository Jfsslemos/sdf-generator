# R84 — Sensibilidade ao registro rígido (13/10/2026)

Experimento exploratório pós-hoc na cena study, sem modificar A0/A2/A2b. ICP robusto ajustado somente em A0 (30.000 pontos) contra o GT oficial (80.000 pontos), três sementes 42/43/44; mesma transformação aplicada a A0/A2/A2b e avaliada em 100.000 pontos independentes por superfície.

Médias Chamfer L1 nativo→rígido: A0 0.089768→0.067746, A2 0.093829→0.071292, A2b 0.088713→0.064764. F@0.02: A0 0.142034→0.421196; A2 0.116174→0.428335; A2b 0.119773→0.463845. Norma de translação ~0.0349 unidade, dominada por Y negativo; rotação ~0.24°. Controle Y oposto piora Chamfer A0 a 0.122936. Ajuste utiliza GT, portanto NÃO substitui o protocolo primário R71, não comprova erro de calibração nem valida física/Gazebo. Escala física não certificada.

Pacote local reproduzível R84 contém código, PLYs com SHA, CSV/JSON, figuras, manuscrito LaTeX atualizado e testes. Sem treino, Gazebo ou COLMAP.
