## Utilitários de projeto: divisor e downloader de arquivos

Este repositório inclui dois scripts Python poderosos projetados para gerenciar a distribuição e download de arquivos grandes por meio de versões do GitHub.

1. **`split_and_hash.py`**: Um utilitário para proprietários de repositórios dividirem arquivos grandes em partes menores e gerarem um manifesto de soma de verificação completo e verificável.
2. **`download_all_packages.py`**: Uma ferramenta robusta para os usuários finais baixarem, verificarem e remontarem automaticamente esses arquivos de várias partes, garantindo a integridade dos dados do início ao fim.

---

### 1. Script de divisão de arquivos e geração de soma de verificação (`split_and_hash.py`)

Este script é destinado ao **mantenedor do repositório**. Ele prepara arquivos grandes para distribuição em plataformas como GitHub Releases, que possuem limites individuais de tamanho de arquivo.

#### Propósito

O objetivo principal é pegar um único arquivo grande (por exemplo, `vosk-model-de-0.21.zip`) e executar duas ações críticas:
1. Divida o arquivo em uma série de partes menores e numeradas.
2. Gere um arquivo de manifesto único e abrangente (`.sha256sums.txt`) que contém as somas de verificação para **o arquivo original completo e cada parte individual**.

Este manifesto completo é a chave para garantir 100% de integridade dos dados para o usuário final.

#### Principais recursos

* **Divisão padronizada:** Divide arquivos em blocos de 100 MB (configuráveis no script).
* **Nomenclatura consistente:** Cria peças com um prefixo `Z_` (por exemplo, `Z_vosk-model-de-0.21.zip.part.aa`). O prefixo `Z_` garante classificação e manuseio adequados em vários sistemas.
* **Manifesto de integridade completo:** O arquivo `.sha256sums.txt` gerado é estruturado para máxima confiabilidade. Inclui:
* O hash SHA256 do **arquivo completo original**.
* O hash SHA256 de **cada parte** que foi criada.

#### Uso para uma versão do GitHub

1. Coloque o arquivo grande (por exemplo, `vosk-model-de-0.21.zip`) em um diretório com o script `split_and_hash.py`.
2. Execute o script em seu terminal:
    ```bash
    python split_and_hash.py <your-large-file.zip>
    ```
3. O script irá gerar todos os arquivos `Z_...part.xx` e o arquivo `...sha256sums.txt` correspondente.
4. Ao criar uma nova versão do GitHub, carregue **todos** os arquivos gerados: os arquivos de parte e o arquivo de manifesto único.
5. Repita esse processo para cada arquivo grande que deseja distribuir.

---

### 2. Downloader e verificador automatizado de pacotes (`download_all_packages.py`)

Este script é destinado ao **usuário final**. Ele fornece uma solução simples de um comando para baixar e remontar com segurança todos os pacotes oferecidos na versão do GitHub.

#### Propósito

Ele automatiza o processo complexo e sujeito a erros de baixar dezenas de partes de arquivos, verificar cada uma delas e remontá-las corretamente. Ele usa os manifestos de soma de verificação fornecidos no lançamento para garantir que o arquivo final montado seja uma cópia perfeita e não corrompida do original.

#### Principais recursos

* **Descoberta automática:** O script se conecta à API do GitHub para encontrar automaticamente todos os "pacotes" disponíveis na versão, procurando por arquivos `.sha256sums.txt`. Nenhuma configuração manual de nomes de arquivos é necessária.
* **Processo de Integridade em Primeiro Lugar:** Para cada pacote, ele baixa o arquivo de manifesto *primeiro* para obter a lista de partes necessárias e suas somas de verificação corretas.
* **Verificação parte por parte:** Ele baixa uma parte de cada vez e verifica imediatamente seu hash SHA256.
* **Repetição automática em caso de corrupção:** Se uma parte baixada estiver corrompida (o hash não corresponde), o script a exclui automaticamente e a baixa novamente, garantindo um download limpo.
* **Remontagem Inteligente:** Depois que todas as partes de um pacote são baixadas e verificadas, ele as mescla na ordem alfabética correta (`.aa`, `.ab`, `.ac`...) para reconstruir o grande arquivo original.
* **Verificação final:** Após a remontagem, ele calcula o hash SHA256 do arquivo final completo e o verifica em relação ao hash mestre encontrado no manifesto. Isso fornece confirmação de sucesso de ponta a ponta.
* **Resiliente e tolerante:** O script é robusto contra pequenas inconsistências de nomenclatura, como `Z_` vs. `z_`, garantindo uma experiência de usuário tranquila.
* **Limpeza automatizada:** Depois que um pacote é compilado e verificado com sucesso, o script exclui os arquivos de peças baixados para economizar espaço em disco.

#### Pré-requisitos

O usuário deve ter o Python e as bibliotecas `requests` e `tqdm` instaladas. Eles podem ser instalados com pip:
```bash
pip install requests tqdm
```

#### Uso

1. Baixe o script `download_all_packages.py`.
2. Execute-o no terminal sem argumentos:
    ```bash
    python download_all_packages.py
    ```
3. O script cuidará do resto, exibindo barras de progresso e mensagens de status. Após a conclusão, o usuário terá todos os arquivos ZIP verificados e finais prontos para uso no mesmo diretório.