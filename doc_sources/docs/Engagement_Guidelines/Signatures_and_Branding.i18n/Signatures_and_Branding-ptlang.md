# Guia de comunicação: assinaturas e branding

Para ajudar a divulgar o **Aura** sem sermos intrusivos, usamos uma estratégia de "branding passivo" por meio de assinaturas de bate-papo. Isso permite que os usuários encontrem o projeto facilmente, mantendo a conversa focada no conteúdo.

## 1. A Assinatura da Aura
Ao usar os recursos de tradução ou automação em um chat, o Aura pode anexar uma pequena assinatura às suas mensagens.

**Formato recomendado:**
> `🗣SL5net ⟫ Aura`

### Divisão dos Símbolos:
* **`🗣` (Speaking Head):** Um indicador visual de que esta mensagem foi processada ou traduzida. Sinaliza "Comunicação/Linguagem".
* **`SL5net`:** O namespace exclusivo. Isso é crucial para a capacidade de pesquisa.
* **`⟫` (colchete direito duplo):** Um símbolo técnico de "pipe" que se parece com um operador CLI/Shell, reforçando que se trata de uma ferramenta técnica.
* **`Aura`:** O nome do projeto.

---

## 2. Por que "SL5net Aura" em vez de um link?
Muitas plataformas de bate-papo (Matrix, Discord, Telegram, etc.) possuem filtros rígidos contra URLs ou estruturas semelhantes a domínios.
* **Pesquisabilidade:** Pesquisar por `SL5net Aura` no Google ou GitHub gera uma taxa de sucesso de 100% para encontrar o repositório.
* **Filtro Seguro:** Ao usar um termo de pesquisa exclusivo em vez de um link `.com`, evitamos ser sinalizados como "spam" ou "bots de anúncios" por moderadores automatizados.
* **Baixa fricção:** É fácil de ler e digitar em uma barra de pesquisa.

---

## 3. Etiqueta de assinatura (FAQ)
Como usar assinaturas de forma eficaz sem incomodar seus parceiros de bate-papo:

### P: Devo ter a assinatura em todas as mensagens?
**R:** Não. Assinaturas constantes podem ser percebidas como spam em bate-papos rápidos.
* **Prática recomendada:** Ative a assinatura apenas para a primeira mensagem em uma nova conversa ou para mensagens traduzidas de "alto valor" específicas.
* **Configuração:** Use o botão `# signatur` em sua configuração para desligá-lo em reuniões de negócios privadas ou altamente formais.

### P: Por que não usar caracteres Braille ou Unicode complexos?
**R:** Testamos símbolos como `⠠de╱Aura`. Embora pareçam únicos, são difíceis para outras pessoas copiarem, colarem ou digitarem manualmente em um mecanismo de pesquisa. `SL5net Aura` é a ponte "Human-to-Search-Engine" mais robusta.

### P: O Emoji (🗣) é profissional o suficiente?
**R:** Em 95% dos ambientes de desenvolvimento modernos (GitHub, Discord, Slack), os emojis são padrão. Se você estiver em um ambiente corporativo de alta conformidade (por exemplo, bancos), recomendamos uma versão mais limpa:
`[Aura SL5net]`

---

## 4. Exemplos de configuração (em config/settings.py ou config/settings_local.py)
Aura oferece suporte a diferentes estilos para combinar com sua personalidade:

```bash
# Professional/Technical
signatur='🗣SL5net ⟫ Aura'

# Discreet/Official
signatur='🗣[ SL5net Aura ]'

# Minimalist
signatur='🗣SL5net Aura'
```

---

### Dica profissional para desenvolvedores:
Ao incluir este guia em seu repositório, você demonstra **"Inteligência Social".** Você não está apenas construindo uma ferramenta; você está construindo uma ferramenta que entende o contexto social de onde ela é usada. Esta é uma qualificação de alto nível frequentemente procurada por **Gerentes de Teste Sênior** e **Proprietários de Produto**.

**🗣SL5net ⟫Aura**