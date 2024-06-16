## Jogo de Tic-Tac-Toe Multijogador em Python 

Este projeto implementa um jogo da velha multijogador com uma arquitetura de servidor-cliente. O servidor gerencia os estados do jogo usando Redis, enquanto os clientes se conectam via sockets e interagem através de uma interface gráfica construída com Tkinter. Este inclui tambem um chat para envio de mensagens entre os jogadores e tambem um ranking dos jogadores.

### Funcionalidades

- Suporte Multijogador: Dois jogadores podem se conectar e jogar um contra o outro em maquinas diferentes.
- Os usuários podem se registrar e fazer login.
- Contém banco de dados da MongoDB que armazena as informações dos usuários e rankings.
- O estado do jogo é armazenado no Redis com expiração periódica para garantir a atualidade.
- Detecta automaticamente o vencedor ou empate
- Reinicia o jogo automaticamente após o término de cada partida
- Os jogadores podem enviar mensagens uns aos outros durante o jogo.
- Dispõe de uma tabela com o ranking dos jogadores que estivem em jogo.

### Requisitos
- Python 3.x
- Servidor Redis em execução localmente na porta padrão (6379)
- Bibliotecas Python: socket, threading, json, tkinter, redis
- MongoDB

### Instalação:

**1-Python**

**Em Windows**

1. Baixe o Instalador do Python:

Vá para o site oficial do Python: python.org
Baixe a versão mais recente do instalador do Python para Windows.

2. Execute o Instalador:

Execute o arquivo baixado.
Marque a opção "Add Python to PATH" (Adicionar Python ao PATH).
Clique em "Install Now" (Instalar Agora).

3. Verifique a Instalação:

Abra o Prompt de Comando (Command Prompt). Digite 

    python --version 

Pressione Enter. Você deve ver a versão do Python instalada.
Também pode verificar o pip, que é o gerenciador de pacotes do Python, digitando 

    pip --version.


**MacOS**

1. Instale o Homebrew (se ainda não estiver instalado):

Abra o Terminal e digite:

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2. Instale o Python usando o Homebrew:

No Terminal, digite:

    brew install python

3. Verifique a Instalação:

No Terminal, digite 

    python3 --version 
    
Para verificar a versão do Python. Verifique o pip com 

    pip3 --version.



**Linux (Ubuntu)**

1. Atualize a Lista de Pacotes:

    sudo apt update

2. Instale o Python:

Para instalar o Python 3:

    sudo apt install python3

Para instalar o pip:

    sudo apt install python3-pip

3. Verifique a Instalação: Digite no Terminal.

    python3 --version

Verifique o pip com 
    pip3 --version.



**2-Redis**

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


**3-MongoDB**

**-Em Sistemas Unix/Linux (Ubuntu/Debian)**

1. Importe a chave pública usada pelo sistema de gerenciamento de pacotes:


    wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -

2. Crie um arquivo de lista para o MongoDB:

    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" 
    sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

3. Atualize o banco de dados de pacotes do sistema:

    sudo apt-get update

4. Instale os pacotes do MongoDB:

    sudo apt-get install -y mongodb-org

5. Inicie o MongoDB:

    sudo systemctl start mongod

6. Verifique o status do MongoDB:

    sudo systemctl status mongod

7. Configure o MongoDB para iniciar automaticamente na inicialização:

    sudo systemctl enable mongod


**Para Windows** 

1. Baixe o instalador do MongoDB:

Acesse o site oficial do MongoDB e baixe a versão mais recente do instalador MSI para Windows.
Execute o instalador:
Siga as instruções do instalador. Certifique-se de selecionar "Complete" para uma instalação completa e marque a opção "Install MongoDB as a Service".

Configure as variáveis de ambiente (opcional):
Adicione o caminho C:\Program Files\MongoDB\Server\<versão>\bin ao PATH do seu sistema para acessar os comandos do MongoDB a partir do prompt de comando.

2. Inicie o MongoDB:

O MongoDB será instalado como um serviço e será iniciado automaticamente. Você pode verificar o serviço através do Services no Windows ou usando o Prompt de Comando:

    net start MongoDB

3. Verifique a instalação:
Abra um terminal ou Prompt de Comando e digite:

    mongo --version


**Para macOS**

1. Instale o Homebrew (se ainda não estiver instalado):

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2. Adicione o repositório do MongoDB ao Homebrew:

    brew tap mongodb/brew

3. Instale o MongoDB:

    brew install mongodb-community@4.4

4. Inicie o MongoDB:

    brew services start mongodb/brew/mongodb-community

5. Verifique a instalação:

    mongo --version

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
- Ainda no terminal, insira o endereço IP do servidor e a porta (por exemplo, 127.0.0.1 e 65432).
- Após isso uma janela irá se abrir onde voce pode fazer o seu login
- Faça o login caso já tenha feito o registo, caso não tenha feito, faça o registo para poder fazer o login e iniciar o jogo. 
E agora já podem jogar e trocar mensagens entre si.

**Contribuição**

Sinta-se à vontade para contribuir com melhorias para este projeto. Você pode abrir um pull request ou relatar problemas na seção de issues.

**ATENÇÃO:**
Este jogo ainda está em processamento por isso não se encontra da melhor forma e está sujeita a alteracões a qualquer momento.
