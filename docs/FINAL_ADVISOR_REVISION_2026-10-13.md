# Fechamento para envio ao orientador — 13/10/2026

## Objetivo

Produzir a próxima versão da dissertação como **versão efetivamente enviável ao orientador**, sem linguagem de rascunho, pendência ou promessa de execução futura no corpo científico.

Fonte de entrada:
- `Dissertacao_COLMAP_Integrado_2026-10-13.zip`
- PDF correspondente de 41 páginas
- captura colorida real do Gazebo já incorporada
- resultados e auditorias registradas nesta branch

Não executar novamente DM-NeRF, COLMAP ou G4.

## Regra editorial principal

O texto deve descrever apenas:
1. o que foi feito;
2. o que foi observado;
3. o que ficou fora do escopo;
4. as limitações do desenho experimental.

Remover formulações semanticamente equivalentes a:
- “será feito”;
- “quando estiver disponível”;
- “ainda falta”;
- “etapas necessárias para fechar”;
- “não integra os resultados desta versão”;
- “se for executado”;
- “resultado ainda não disponível”.

Quando algo não foi realizado por decisão de escopo, escrever como **fora do escopo**, não como pendência.

## Correções obrigatórias já identificadas

### Introdução
- Seção 1.3: remover a frase que afirma que COLMAP não integra os resultados. O baseline foi executado e faz parte da avaliação.
- Reescrever 1.3 para tornar a contribuição explícita em linguagem acessível:
  - caracterização rastreável DM-NeRF -> geometria explícita -> objetos independentes -> Gazebo;
  - contrato explícito topologia/IDs e tratamento de faces de fronteira;
  - seleção geométrica auditável e regularização condicionada do piso;
  - avaliação separada de imagem, geometria e uso funcional, incluindo COLMAP e Gazebo.
- Seção 1.4: remover “resultados disponíveis” e “etapas ainda necessárias para fechar a avaliação funcional”. Descrever simplesmente a organização final dos capítulos.

### Protocolo
- Seção 4.2: trocar “quando o runtime estiver disponível” por descrição factual da avaliação A2 no runtime.
- Remover G4 do protocolo, resultados, limitações e conclusão. Ele não compõe a evidência necessária e sua presença como “não executado” cria aparência de trabalho inacabado.
- Em 4.7, manter apenas G0–G3.
- Definir em linguagem simples:
  - IoU e AP;
  - Multi-View Stereo (MVS);
  - RANSAC;
  - PQscene (maior é melhor; mede qualidade panóptica da cena no protocolo citado).
- Incluir MVS, RANSAC e URDF na lista de siglas se permanecerem no texto.

### Resultados
- Seção 5.3: corrigir “três vistas” para quatro.
- Seção 5.4: remover “duas vistas”; a figura atual contém uma vista.
- G3: substituir qualquer formulação que sugira precisão física micrométrica. A diferença de ~4 µm deve ser descrita apenas como **concordância numérica entre a pose registrada da face inferior e a altura calculada do plano**. O resultado funcional é: a caixa caiu, foi interrompida pela superfície e permaneceu estável.
- Tabela de Gazebo: remover linha G4.
- Não usar “não executado” para etapa que não faz parte do escopo final.

### Discussão e conclusão
- Remover “trabalho futuro”, “como continuidade, pode ser repetida...” e equivalentes.
- Reescrever como limitação fechada:
  - “O estudo não avalia variabilidade entre cenas.”
  - “A análise não cobre estimação de propriedades físicas/articulações.”
  - “A configuração COLMAP não foi ajustada por cena.”
- Não sugerir que a dissertação depende de experimentos adicionais.
- Conclusão deve terminar respondendo a pergunta de pesquisa e delimitando a validade, sem lista de tarefas futuras.

### Bibliografia
- Corrigir `Sch"onberger` para `Schönberger` ou codificação LaTeX equivalente correta.
- Fazer varredura de capitalização/nomenclatura: NeRF, DM-NeRF, NeuS, NICE-SLAM, COLMAP, URDF, Gazebo Classic.

## Figuras — evitar repetição e tornar autoexplicativas

### Repetições a remover
A versão atual repete conteúdo visual:
- as quatro RGB de entrada aparecem isoladamente e voltam a aparecer como linha de referência na comparação referência x render;
- A0 aparece isoladamente e novamente no painel referência x A0 x COLMAP.

Para a versão do orientador:
- remover a figura isolada de vistas RGB; usar a comparação referência x render como primeira evidência visual da cena;
- remover a figura isolada A0; usar a comparação referência x A0 x COLMAP como evidência qualitativa principal de geometria;
- renumerar figuras e chamadas automaticamente.

### Comparação COLMAP
Manter a comparação qualitativa Referência DM-SR x DM-NeRF A0 x COLMAP, mas adicionar **subcaptions fora das áreas de dados**:
- (a) Referência DM-SR
- (b) DM-NeRF A0
- (c) COLMAP

Não desenhar texto sobre os pontos.

Não criar/renderizar uma segunda vista artificial. Só acrescentar segunda vista se puder ser derivada deterministicamente dos dados reais já disponíveis.

### Demais figuras
- manter mapa de instâncias GT x predição;
- manter A1 colorida por ID;
- manter resíduos A1 x A2;
- manter captura colorida real do Gazebo;
- manter gráfico F-score se a tabela não tornar a página excessivamente redundante;
- nenhum texto/legenda deve ficar sobreposto à área de dados;
- verificar que não há imagem idêntica usada duas vezes sem justificativa explícita.

## Linguagem para banca não especializada

Cada seção de resultados deve responder, nessa ordem, sem jargão desnecessário:
1. o que está sendo medido;
2. qual é a direção desejável da métrica;
3. qual foi o valor observado;
4. o que esse valor significa no contexto da cena;
5. o que ele não permite concluir.

Evitar hiperboles e adjetivos avaliativos.

## Auditoria final antes de disponibilizar o PDF

Executar busca no PDF compilado por:
- “não integra”
- “quando o runtime”
- “ainda necessária”
- “resultados disponíveis”
- “não executado”
- “trabalho futuro”
- “como continuidade”
- “se for executado”
- “pendente”
- “a realizar”

Nenhuma ocorrência com sentido de pendência do trabalho deve permanecer.

Também verificar:
- referências e citações resolvidas;
- chamadas Figura/Tabela consistentes;
- número de vistas consistente com a figura;
- ausência de duplicatas visuais involuntárias;
- nenhuma imagem cortada;
- nenhum texto sobreposto;
- listas de figuras/tabelas atualizadas;
- PDF A4 e institucional;
- todas as páginas renderizadas e inspecionadas visualmente.

## Git

Trabalhar somente em `work-codex-2026`.
Nunca alterar `master` ou `dissertacao-2026`.

Versionar no branch:
- fonte LaTeX final para orientador;
- figuras efetivamente usadas;
- instrução de compilação;
- PDF final do orientador, se o repositório aceitar binários desse porte;
- status atualizado.

Não versionar:
- bundle COLMAP completo;
- normal/depth maps;
- fused.ply completo.

## Critério de pronto

A versão está pronta para o orientador quando puder ser lida como trabalho concluído sob um escopo delimitado, e não como relatório de andamento.
