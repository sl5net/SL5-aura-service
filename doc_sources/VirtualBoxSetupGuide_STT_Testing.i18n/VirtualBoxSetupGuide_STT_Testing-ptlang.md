# Guia de configuração do VirtualBox para testes de projetos STT

Este guia fornece as etapas recomendadas para configurar uma máquina virtual Ubuntu 24.04 estável e de alto desempenho no VirtualBox. Seguir estas instruções criará um ambiente consistente para testar o aplicativo STT e evitará problemas comuns como lentidão na instalação, travamentos do sistema e falta de funcionalidade da área de transferência.

## Pré-requisitos

- VirtualBox instalado na máquina host.
- Um arquivo ISO do Ubuntu 24.04 Desktop baixado.

## Hardware de host de referência

Esta configuração foi testada e validada no sistema host a seguir. O desempenho pode variar em outro hardware, mas as configurações de estabilidade devem ser aplicadas universalmente.

- **Sistema operacional:** Manjaro Linux
- **Núcleo:** 6.6.94
**Processador:** 16 × AMD Ryzen 7 3700X
**Memória:** 31,3 GiB de RAM
**Processador gráfico:** NVIDIA GeForce GTX 1050 Ti

---

## Parte 1: Criação e configuração de VM

Essas configurações são críticas para desempenho e estabilidade.

### Etapa 1.1: Crie a nova máquina virtual

1. No VirtualBox, clique em **Novo**.
2. **Nome:** `Ubuntu STT Tester` (ou similar).
3. **Imagem ISO:** Deixe este campo em branco.
4. Marque a caixa: **"Ignorar instalação autônoma"**.
5. Clique em **Avançar**.
6. **Hardware:**
- **Memória Base:** `4096 MB` ou mais.
- **Processadores:** `4` ou mais.
7. Clique em **Avançar**.

### Etapa 1.2: Crie o disco rígido virtual (CRÍTICO)

Esta é a etapa mais importante para instalação e desempenho rápidos.

1. Selecione **"Criar um disco rígido virtual agora"**.
2. Defina o tamanho do disco para **40 GB** ou mais.
3. Na próxima tela, altere o tipo de armazenamento para **"Tamanho fixo"**.
> **Por quê?** Um disco de tamanho fixo é pré-alocado e evita o grande gargalo de E/S que ocorre quando um disco "alocado dinamicamente" é constantemente redimensionado durante a instalação.
4. Clique em **Criar** e aguarde a conclusão do processo.

### Etapa 1.3: configurações finais da VM

Selecione a VM recém-criada e clique em **Configurações**. Configure o seguinte:

- **Sistema -> Placa-mãe:**
- **Chipset:** `ICH9`
- Marque **"Ativar EFI (somente sistemas operacionais especiais)"**.

- **Exibição -> Tela:**
- **Controlador gráfico:** `VMSVGA`
- **Desmarque "Ativar aceleração 3D"**.
> **Por quê?** A aceleração 3D é uma causa comum de travamentos e travamentos do sistema em convidados Linux. Desativá-lo melhora significativamente a estabilidade.

-   **Armazenar:**
- Selecione o **Controlador SATA**. Marque a caixa **"Usar cache de E/S do host"**.
- Selecione o arquivo do disco virtual (`.vdi`). Marque a caixa **"Unidade de estado sólido"**.
- Selecione a unidade óptica **Vazia**. Clique no ícone do CD à direita e **"Escolha um arquivo de disco..."** para anexar seu Ubuntu 24.04 ISO.

Clique em **OK** para salvar todas as configurações.

---

## Parte 2: Instalação do sistema operacional Ubuntu

1. Inicie a VM.
2. Prossiga com a configuração do idioma e do teclado.
3. Ao chegar em "Atualizações e outros softwares", selecione:
- **Instalação mínima**.
- **Desmarque** "Baixar atualizações durante a instalação do Ubuntu".
4. Continue com a instalação até que esteja concluída.
5. Ao terminar, reinicie a VM. No prompt, remova a mídia de instalação (pressione Enter).

---

## Parte 3: Pós-instalação (adições de convidados)

Esta etapa permite o compartilhamento da área de transferência, arrastar e soltar e redimensionar automaticamente a tela.

### Etapa 3.1: Instale o ISO de adições de convidados no host (se necessário)

Na sua **máquina host**, certifique-se de que o pacote ISO do Guest Additions esteja instalado.

- **No Arco/Manjaro:**
    ```bash
    sudo pacman -S virtualbox-guest-iso
    ```
- **No Debian/Ubuntu:**
    ```bash
    sudo apt install virtualbox-guest-additions-iso
    ```

### Etapa 3.2: Instale adições de convidados dentro da VM Ubuntu

Execute estas etapas **dentro da sua VM Ubuntu em execução**.

1. **Prepare o Ubuntu:** Abra um terminal e execute os seguintes comandos para instalar dependências de compilação.
    ```bash
    sudo apt update
    sudo apt install build-essential dkms linux-headers-$(uname -r)
    ```
2. **Insira o CD:** No menu superior do VirtualBox, vá para **Dispositivos -> Inserir imagem de CD de adições de convidados...**.
3. **Execute o instalador:**
- Poderá aparecer uma caixa de diálogo solicitando a execução do software. Clique em **Executar**.
- Se nenhuma caixa de diálogo aparecer, abra o Gerenciador de Arquivos, clique com o botão direito no CD `VBox_GAs...`, escolha **"Abrir no Terminal"** e execute o comando:
__CODE_BLOCO_3__
4. **Reinicializar:** Após a conclusão da instalação, reinicialize a VM.
      ```bash
      sudo ./VBoxLinuxAdditions.run
      ```
5. **Ativar recursos:** Após a reinicialização, vá para o menu **Dispositivos** e ative **Área de transferência compartilhada -> Bidirecional** e **Arrastar e soltar -> Bidirecional**.

Seu ambiente de teste estável e de alto desempenho está pronto.