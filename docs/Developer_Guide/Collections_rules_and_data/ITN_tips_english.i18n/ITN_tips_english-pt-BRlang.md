O termo técnico é **Normalização de texto inverso (ITN)**.

Se você pesquisar, encontrará enormes coleções de regras e dados.

Aqui estão os melhores recursos para preencher mapas sem digitar tudo sozinho:

### 1. Coleções de regras ITN (o “padrão ouro”)
* **[itnpy](https://github.com/barseghyanartur/itnpy):** Uma ferramenta Python simples e determinística projetada para esse propósito. Ele usa arquivos CSV para converter palavras faladas em caracteres escritos (números, moedas, datas). Você pode copiar os CSVs quase 1:1 em seu mapa.

* **[NVIDIA NeMo ITN](https://github.com/NVIDIA/NeMo):** Muito poderoso. Eles têm enormes arquivos gramaticais para quase todos os idiomas. Lá você encontrará listas de unidades de medida, títulos e formatos de data.

### 2. Fontes de dados para pontuação e maiúsculas e minúsculas
* **[Vosk recasepunc](https://github.com/benob/recasepunc):** Esta é a ferramenta padrão do Vosk. Ele usa modelos, mas o código-fonte geralmente contém listas de abreviações e nomes próprios que podem ser extraídos.

* **[Google Text Normalization Dataset](https://github.com/rwsproat/text-normalization-data):** Um enorme conjunto de dados (criado para um desafio Kaggle) contendo milhões de exemplos de como a linguagem falada é convertida em linguagem escrita.

### 3. Bibliotecas “auxiliares de ditado”
* **[num2words](https://github.com/savoirfairelinux/num2words):** Se precisar de mapeamento de números, você pode encontrar listas de “um” a “um milhão” aqui.