# esclarecendo o comportamento exato do fluxo de trabalho do seu sistema:
  
### Explicação corrigida do fluxo de trabalho integrado

a primeira regra para **Transformação de entrada** e **Rotulagem** antes que a ação de pesquisa final seja executada pela segunda regra.

#### 1. Entrada: "was ist ein haus"

#### 2. Regra 1: Rotulagem/Transformação

```python
("was ist ein haus (Begriffsklärung)", r'^.*was ist ein haus$', 90,
 {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool','fullMatchStop']})
```

* **Ação:** A entrada do usuário `"was ist ein haus"` foi correspondida com sucesso.
* **Resultado (Interno):** O sistema gera a saída/rótulo `"was ist ein haus (Begriffsklärung)"`.
* **Continuação:** Como `fullMatchStop` está na `skip_list`, a regra correspondente **NÃO PARA**. O processo continua para a próxima regra, transportando o conteúdo *transformado* ou *rotulado*.

#### 3. Regra 2: Ação/Execução Geral

```python
('', r'(suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist)( ein| die| das| der)? (?P<search>.*)', 90, {
'flags': re.IGNORECASE,
'on_match_exec': [CONFIG_DIR / 'wikipedia_local.py']
})
```

* **Ação:** O sistema agora provavelmente corresponde ao **resultado/rótulo atual** da etapa anterior, que é `"was ist ein haus (Begriffsklärung)"` (ou corresponde à entrada original, mas o script executado prioriza o rótulo transformado).
* **Correspondência de prefixo:** O prefixo (`was ist`) ainda corresponde.
* **Grupo de Captura:** O grupo de captura `(?P<search>.*)` captura o resto da string:
* Se o sistema usar a saída **Rule 1 como a nova entrada**, ele capturará: **`haus (Begriffsklärung)`** (ou a string completa transformada, que será então analisada pelo script de execução).
* **Execução:** O script `wikipedia_local.py` é executado.

#### 4. Ação Final:

* O script `wikipedia_local.py` recebe o termo/rótulo de pesquisa especificamente modificado.
* O script realiza uma pesquisa na Wikipedia pelo termo pretendido: **`haus (Begriffsklärung)`**.

**Conclusão:**

Essa configuração é uma maneira elegante de lidar com consultas ambíguas ou genéricas. Ao fazer com que a regra específica modifique a entrada ou gere um rótulo direcionado e, em seguida, forçando o processo a continuar com a regra de pesquisa geral, você garante que a pesquisa na Wikipédia seja executada não para o "haus" genérico, mas para a entrada específica e sem ambiguidade: **`haus (Begriffsklärung)`**.

Isso confirma que a exclusão de `fullMatchStop` é **essencial** para permitir que a primeira regra pré-processe e enriqueça a consulta antes que ela seja acionada pela regra de execução de uso geral.

(sl5,4.12.'25 12:24 Qui)