# Work status

Atualizado em 2026-10-05.

## Concluído
- branch de trabalho `dissertacao-2026` criada sem alterar `master`;
- decisões metodológicas e definition of done registradas;
- repositório legado auditado;
- código oficial do DM-NeRF auditado;
- confirmado que DM-SR/DM-NeRF usa RGB + poses + supervisão 2D de instâncias;
- confirmado que a avaliação oficial gera PSNR, SSIM, LPIPS e APs de instância;
- confirmado que o modo de meshing usa uma malha de referência do DM-SR;
- identificada dependência metodológica: essa malha de referência informa o bounding frame do meshing oficial;
- runner para GPU gratuita no Kaggle adicionado;
- notebook Kaggle da cena `study` adicionado;
- ferramentas de avaliação geométrica, planaridade e regularização do piso adicionadas;
- pergunta/objetivos científicos corrigidos em rascunho, sem sobrescrever a dissertação;
- plano experimental reduzido ao caminho crítico.

## Bloqueio externo atual
A execução do DM-NeRF precisa de uma GPU CUDA. Não há GPU no ambiente desta conversa. O próximo passo que depende do usuário é apenas iniciar o notebook Kaggle gratuito com GPU e Internet. Todo o setup seguinte foi automatizado no notebook/runner.

## Próxima sequência
1. smoke test da cena `study` no Kaggle;
2. corrigir qualquer incompatibilidade real encontrada no ambiente gratuito;
3. treino reproduzível/resumível;
4. avaliação oficial;
5. meshing;
6. pós-processamento e ablation do piso;
7. métricas/tabelas;
8. integração no texto.
