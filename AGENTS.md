# AGENTS.md — regras de execução da dissertação

## Objetivo
Transformar o código existente da prova de conceito em uma base reproduzível para os experimentos da dissertação, sem trocar o método principal.

## Decisões congeladas
- O método principal permanece DM-NeRF.
- DM-SR é o conjunto experimental principal enquanto for reproduzível.
- OneFormer, Nerfacto e CAD retrieval não fazem parte do caminho crítico atual.
- SDFormat é apenas mecanismo de serialização/integração com Gazebo, não contribuição científica.
- Gazebo Classic pode ser mantido; não migrar sem necessidade experimental clara.
- Prioridade é concluir com rigor até ~21/10/2026 para envio do texto e ~28/10/2026 para defesa.

## Política para agentes
1. Não reabrir decisões congeladas sem evidência concreta.
2. Não introduzir dependências pesadas ou novos frameworks por conveniência.
3. Cada alteração deve responder a uma pergunta experimental ou melhorar reprodutibilidade.
4. Preferir scripts CLI simples, determinísticos e documentados.
5. Antes de executar em todas as cenas, validar em uma cena e registrar custo/tempo.
6. Se uma tarefa consumir mais de um dia sem progresso mensurável, reportar bloqueio e propor corte/alternativa.
7. Não atribuir ao trabalho métricas/resultados que não tenham origem rastreável.
8. Manter resultados brutos separados de tabelas derivadas.

## Definition of done de uma tarefa técnica
- código executável;
- comando reproduzível;
- entrada/saída documentadas;
- ao menos um smoke test;
- resultado salvo em formato aberto (CSV/JSON/PLY/OBJ etc.);
- impacto na dissertação indicado em uma frase.
