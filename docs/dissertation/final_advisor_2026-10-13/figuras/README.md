# Proveniência das figuras

`method_pipeline.svg` é a fonte vetorial editável do diagrama metodológico. `method_pipeline.pdf` é sua exportação para inclusão no documento. O diagrama resume etapas e medidas descritas no texto e não contém imagens nem resultados adicionais.

`study_scene_reference.png` é um recorte do primeiro painel RGB da linha correspondente à cena `study` em `figs/decomposition_scenes.png`, disponibilizada no repositório oficial do DM-NeRF. O recorte remove apenas os demais painéis da composição original e foi redimensionado para inclusão no documento; não houve geração ou alteração do conteúdo da cena.

As imagens `render_comparison_source.png` e `instance_comparison_source.png` preservam as composições originais produzidas com as vistas 0, 33, 66 e 99 da avaliação oficial.

Para melhorar a leitura sem alterar as evidências, cada composição foi separada em linhas de referência e predição. Em `render_difference_row.png`, cada pixel é a diferença absoluta entre referência e renderização, multiplicada por cinco e limitada ao intervalo de 8 bits. Em `instance_difference_row.png`, magenta identifica pixels cuja cor, que codifica o ID da instância no protocolo, difere entre referência e predição. As legendas e identificadores das linhas são compostos em LaTeX, fora da área das imagens.
