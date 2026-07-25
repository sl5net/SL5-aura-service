# Motivação: Por que “Disco vence”?

## O problema no modo avó Aura

No [Aura Oma Mode](../../../GettingStarted.i18n/GettingStarted-pt-BRlang.md) (ver linha 67), Aura opera em grande parte de forma autônoma:
o usuário fala os comandos e o Aura grava nos arquivos por conta própria —
configurações, scripts, entradas de log, texto gerado.

O seguinte cenário acontece constantemente:

1. O usuário possui um arquivo aberto no editor (por exemplo, um arquivo de regras ou um script).
2. Eles esquecem que o editor ainda está ativo e falam um comando do Aura.
3. Aura altera o arquivo no disco.
4. O editor detecta a mudança externa — e **pergunta**.

Este prompt é um **empecilho** no modo Oma:
- O usuário pode estar sentado no sofá, usando entrada de voz,
e não consegue ver ou acessar a caixa de diálogo.
- Ou eles pressionaram acidentalmente uma tecla no editor, o buffer agora está
"modificado", e toda alteração externa é bloqueada com um
"Recarregar? / Manter local?" diálogo.
- O resultado: Aura continua funcionando, mas o editor mostra uma versão obsoleta.
O usuário pensa que está vendo o arquivo atual, mas edita com base
num estado antigo – o caos é garantido.

## O que precisamos

Comportamento do editor que **sempre prioriza o disco**.
Quando o Aura (ou qualquer outra ferramenta) altera o arquivo, o editor deve
imediatamente e **sem qualquer aviso** mostre o novo conteúdo.
A entrada não salva no editor pode ser descartada silenciosamente - porque em
Modo Oma, Aura é a fonte da verdade, não a entrada humana do teclado.

## Por que os editores padrão falham

Quase todos os editores comuns (Kate, VS Code, Sublime Text, Notepad++,
Emacs, Vim, CudaText prontos para uso) possuem um mecanismo de proteção:
assim que o buffer contém alterações não salvas, eles **sempre** perguntam
quando ocorre uma mudança externa. Este é um recurso normal
trabalho de desenvolvedor – mas um bug para o modo Aura Oma.

Este plugin fecha exatamente essa lacuna para CudaText.

## Público-alvo

- Usuários do Modo Aura Oma que visualizam arquivos em um editor em paralelo.
- Cenários de automação onde um processo grava arquivos e um editor
serve apenas como um visualizador ao vivo.
- Qualquer pessoa para quem “o disco sempre vence” é o comportamento desejado.