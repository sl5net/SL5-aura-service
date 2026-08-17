# Plugin CudaText: "Disk Wins" (Forçar recarga automática em alterações externas)

CudaText não tem nenhuma opção integrada que recarrega silenciosamente um arquivo no momento em que ele
alterações no disco - cada modo integrado "alterado no disco" ainda mostra algumas
tipo de prompt (modal ou sem modal) antes de recarregar
(veja `ui_notif_confirm` em `default.json`, valores `0`-`4`, todos os quais
perguntar). Este plugin preenche essa lacuna: **o disco sempre vence**, sem prompt, nunca.

Arquivado aqui para que ninguém precise derivar novamente a API do plugin CudaText para isso
de novo. A fonte da verdade do próprio plugin reside em
[`cuda_disk_wins/`](.././cuda_disk_wins/) nesta pasta.

## O que faz

- Pesquisa todos os arquivos abertos e nomeados uma vez por segundo (configurável via
`TIMER_INTERVAL` em `__init__.py`).
- Se o mtime de um arquivo no disco for alterado, o plugin o relê e chama
`Editor.set_text_all()` — **substituindo quaisquer alterações não salvas no
guia do editor sem perguntar**.
- Apaga o flag "modificado" posteriormente (`PROP_MODIFIED = False`), então o
tab parece limpa, como se nada tivesse divergido.
- O melhor esforço restaura a posição do cursor e a linha visível superior após
recarregar.
- Adiciona dois comandos em `Plugins → Disk Wins`:
- `Ativar/desativar recarga automática`
- `Verificar agora` (verificação manual única)

## Por que um plugin em vez de uma configuração

O próprio observador de arquivos do CudaText (`ui_notif`) oferece apenas comportamentos de "pergunta":

| `ui_notif_confirm` | Comportamento |
|---------------------|------------------------------------------------------------------|
| 0 | prompt sem modal, sempre |
| 1 | prompt sem modal, se o editor foi modificado ou Desfazer não está vazio |
| 2 | prompt sem modal, se o editor for modificado |
| 3 | prompt modal, sempre |
| 4 | prompt modal, se o editor for modificado |

Não há valor que signifique "recarregar automaticamente, sem aviso, continue".
Daí este pequeno plugin, que executa seu próprio loop de pesquisa e recarrega
diretamente por meio da API Python.

## Instalação

```bash
mkdir -p ~/.config/cudatext/py
cp -r cuda_disk_wins ~/.config/cudatext/py/
```

Reinicie o CudaText.

**Importante:** desative também a caixa de diálogo de notificação de alterações do próprio CudaText para
não briga com o plugin. Em
`~/.config/cudatext/settings/user.json`:

```json
{
    "ui_notif": false
}
```

(Equivalente a `Opções → Configurações – configuração do usuário` na UI.) Reinicie
CudaText novamente após esta alteração.

## Advertências

- Isto é intencionalmente destrutivo: edições não salvas do editor são descartadas
silenciosamente no momento em que o arquivo é alterado externamente. Isso é tudo
ponto do plugin - não o instale se às vezes quiser manter
edições locais sobre alterações externas.
- Reage apenas a alterações no mtime do arquivo; digitando no próprio editor
não aciona uma recarga (sem ciclo de feedback).
- Se o arquivo for excluído externamente, o plugin não fará nada até
reaparece (sem travamento, sem tentativas repetidas de recarga).
- A codificação é lida via `PROP_ENC` e mapeada para o codec Python mais próximo;
estenda `ENC_MAP` em `__init__.py` se você ainda não usa uma codificação
listado.

## Origem

Construído para "sempre preferir alterações no sistema de arquivos ao editor não salvo
buffers, sem confirmação" requisito discutido ao configurar o CudaText
via `yay -S cudatext-qt6-bin python` no Arch.