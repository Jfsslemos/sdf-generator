# Revisão crítica em modo de banca — 13/10/2026

## Parecer resumido

O trabalho agora possui uma cadeia experimental completa para a cena `study` e uma comparação externa quantitativa/qualitativa. O argumento científico está defensável, desde que seja apresentado como **caracterização experimental de uma cadeia de estruturação para simulação**, e não como novo método neural ou benchmark geral.

A versão ainda precisa de uma revisão editorial curta antes de ser enviada ao orientador.

## O que um avaliador não especialista consegue entender

A sequência geral é compreensível:
1. DM-NeRF reconstrói e decompõe a cena;
2. A0 mede a geometria extraída;
3. A1 transforma IDs em objetos separados;
4. A2 regulariza uma superfície candidata a piso;
5. Gazebo verifica carregamento, independência e contato.

O resumo e a conclusão conseguem responder “o que foi feito”, “o que funcionou” e “o que não pode ser concluído”.

## Pontos fortes

- pergunta de pesquisa explícita e não binária;
- separação entre métricas de imagem, geometria e função no simulador;
- reprodução do DM-NeRF confrontada com os números publicados na mesma cena;
- baseline COLMAP executado e auditado no mesmo suporte;
- limites de comparabilidade declarados;
- A1 avaliada por estrutura, não por métrica que ela não altera;
- A2 não é vendida como ganho de fidelidade;
- limitações de uma única cena e de malhas não estanques aparecem no texto;
- G3 é tratado como evidência pontual, não como validação física global.

## Pontos que uma banca provavelmente questionaria

### 1. Qual é exatamente a contribuição?

A contribuição atual está correta, mas precisa ficar explícita em linguagem simples logo na introdução. Recomenda-se listar 3--4 contribuições concretas:
- caracterização reproduzível da passagem DM-NeRF -> geometria explícita -> objetos independentes -> Gazebo;
- contrato auditável de associação entre topologia e IDs de instância, incluindo faces de fronteira;
- seleção geométrica rastreável e regularização condicionada do piso;
- avaliação externa de geometria e validação funcional no simulador.

### 2. Por que uma única cena é suficiente?

Não é suficiente para generalização. O texto reconhece isso corretamente. Na defesa, a resposta deve ser: a unidade experimental é um estudo de caso reproduzível; os 200 mil pontos não são 200 mil amostras independentes. A conclusão é “funcionou nesta cena sob este protocolo”, não “funciona em ambientes domésticos em geral”.

### 3. Por que comparar com COLMAP?

Porque fornece uma referência geométrica externa que não depende do mesmo campo neural. Não é comparação panóptica nem real-to-sim completa. O valor está em mostrar que a geometria A0 não é avaliada somente contra si mesma ou por métricas de imagem.

### 4. A comparação com COLMAP é justa?

É controlada, não definitiva: mesmas poses/intrínsecos, mesmo suporte espacial e cardinalidade de avaliação. Ainda assim, o COLMAP não foi ajustado por cena e `min_num_pixels=1` favorece completude. Essa ressalva deve permanecer visível.

### 5. O contato do Gazebo tem precisão micrométrica?

Não deve ser formulado assim. A diferença de ~4 µm é apenas a diferença numérica entre a pose final registrada e a altura calculada do plano. Não demonstra precisão física micrométrica do motor de física.

## Problemas editoriais encontrados

- capítulo 1 contém texto anterior ao fechamento do COLMAP e do runtime;
- Figura 3: texto diz três vistas, figura tem quatro;
- Figura 4: texto diz duas vistas, figura atual tem uma;
- referência `Sch"onberger` está incorreta;
- Figura 5 precisa de rótulos externos/subcaptions para leitores não especialistas.

## Critério para envio ao orientador

Enviar depois de corrigir os cinco problemas editoriais acima e melhorar a autoexplicação da Figura 5. Não é necessário executar novos experimentos, COLMAP, DM-NeRF ou G4 para essa rodada.
