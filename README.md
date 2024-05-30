## Jogo de Tic-Tac-Toe Multijogador em Python 

Este projeto implementa um jogo da velha multijogador com uma arquitetura de servidor-cliente. O servidor gerencia os estados do jogo usando Redis, enquanto os clientes se conectam via sockets e interagem através de uma interface gráfica construída com Tkinter.

### Recursos

- Suporte Multijogador: Dois jogadores podem se conectar e jogar um contra o outro.
- Estado do Jogo Persistente: O estado do jogo é armazenado no Redis com expiração periódica para garantir a atualidade.
- Detecta automaticamente o vencedor ou empate
- Reinicia o jogo automaticamente após o término de cada partida
- Comunicação em Tempo Real: Os jogadores podem enviar mensagens uns aos outros durante o jogo.

### Requisitos
- Python 3.x
- Servidor Redis em execução localmente na porta padrão (6379)
- Bibliotecas Python: socket, threading, json, tkinter, redis

### Instalação:

**-Em Sistemas Unix/Linux (Ubuntu/Debian)**
1. Atualize os pacotes do sistema:

    sudo apt update
    sudo apt upgrade

2. Instale o Redis:

    sudo apt install redis-server
    
3. Verifique a instalação:

    redis-cli --version

4. Inicie o serviço Redis:

    sudo systemctl start redis-server

5. Habilite o Redis para iniciar na inicialização do sistema:

    sudo systemctl enable redis-server


**Em MacOS:**

1-Instale o Homebrew (se você não tiver o Homebrew instalado):

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2-Instale o Redis usando o Homebrew:

    brew install redis

3-Inicie o serviço Redis:

    brew services start redis

4-Verifique a instalação:

    redis-cli --version

**Em Windows:**

Para instalar o Redis no Windows, você pode usar o WSL (Windows Subsystem for Linux) ou baixar um binário do Redis nativo para Windows.

Usando WSL (Windows Subsystem for Linux)
Habilite o WSL e instale uma distribuição Linux (por exemplo, Ubuntu):

Siga as instruções da Microsoft para instalar o WSL: Guia de instalação do WSL
Abra o terminal WSL (Ubuntu) e siga as instruções para sistemas Unix/Linux mencionadas acima.

Usando Binários do Redis para Windows
1. Baixe o Redis para Windows:

Acesse [Redis no GitHub (microsoftarchive/redis)](https://docs.microsoft.com/pt-br/windows/wsl/install) e baixe a versão mais recente do Redis.

2. Extraia o arquivo ZIP e execute o `redis-server.exe:`

    -Extraia os arquivos para um diretório de sua escolha.
    -Abra um terminal no diretório onde você extraiu os arquivos.
    -Execute o `redis-server.exe` .

3. Verifique a instalação:

    -Abra outro terminal no mesmo diretório e execute redis-cli.exe para interagir com o servidor Redis.

**Verificação**
Independente do sistema operacional, você pode verificar se o Redis está funcionando corretamente executando o comando:

    redis-cli ping

Você deve receber a resposta PONG.

**Instale as dependências do Python:**

    pip install redis

### Execução
Ao terminar a parte da instalação passe para a execução do codigo

**Servidor do Jogo**
Inicie o servidor:

    python server_fitxe-fatxe.py

O servidor estará escutando conexões na porta 65432.

**Player**
Iniciar o player:

    python player.py

Conecte ao servidor:
- Escolha qual player irá jogar
- Insira o endereço IP do servidor e a porta (por exemplo, 127.0.0.1 e 65432). 
E agora já podem jogar e trocar mensagens entre si.
**Contribuição**

Sinta-se à vontade para contribuir com melhorias para este projeto. Você pode abrir um pull request ou relatar problemas na seção de issues.

**ATENÇÃO:**
Este jogo ainda está em processamento por isso não se encontra da melhor forma e está sujeita a alteracões a qualquer momento.
