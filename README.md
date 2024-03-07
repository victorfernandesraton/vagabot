# Vagabot - Buscando e comentando em posts do linkedin

## Disclaimer

Este projeto consiste em um webcrawler usando Selenium e simulando o comportamento de um usuário no linkedin, ainda que sejam feitos aguns ajustes para que o mesmo não seja detectado como bot pelo linkedin, não há forma de garantir que este projeto possa causar problemas legais ou bloqueio de sua conta __USE POR CONTA E RISCO__

## Introdução

O vagabot é um projeto que consiste em automatizar o processo de buscar postagens referentes a vaga de emprego, adicionar o autor e comentar nestas postagens, assim aumentando o seu alcance como candidato

## O que você precisa para testar
- Logar no seu navegador padrão com sua conta do linkedin __ANTES__ e __DURANTE__ o uso do bot para evitar detecção de login suspeito
- Mudar a configuração da sua conta para inglês (Recomendado , mas não obrigatório)
- Docker e Docker compose

## Instalação
O projeto foi feito todo para rodar em ambiente docker, sem precisar de ajustes , mas você pode rodar ele na sua maquina host subindo apenas os containeres do Selenium grid

### No ambiente docker
Basta contruir o container do projeto com:

```bash
# constroi o projeto
docker-compose build
# sobe os serviços
docker-compose up
```

Depois basta usar o cli a partir do comando docker compose run

```bash
# lista os helpers do cli
docker-compose run worker --help

# Faz uma busca por postagens usando a query "Vaga AND javascript AND remoto" sendo -u e -p email de login e senha do linkedin
docker-compose run worker search-posts -u <email> -p <password> -q "Vaga AND javascript AND remoto"

# Realiza comentários em postagens que ainda não interagiu usando o texto "Gostaria de participar, entre em contato comuigo pelo direct" sendo -u e -p email de login e senha do linkedin
docker-compose run worker post-comment -u <email> -p <password> -c "Gostaria de participar, entre em contato comuigo pelo direct"

```
### No ambiente python

__AVISO__: Este modo considera que você sabe o que está fazendo

Basta contruir o container do projeto com:

```bash
# constroi o projeto
docker-compose build
# sobe os serviços
docker-compose up
```

Depois basta construir o CLI com base no Dockerfile usando o poety como ferramenta de distribuição

```bash
# Inicia um ambiente virtual de sua preferência
pipx run poetry shell

# Instala as dependencias
poetry install

# lista os helpers do cli
python script.py --help

# Faz uma busca por postagens usando a query "Vaga AND javascript AND remoto" sendo -u e -p email de login e senha do linkedin
python search-posts -u <email> -p <password> -q "Vaga AND javascript AND remoto"

# Realiza comentários em postagens que ainda não interagiu usando o texto "Gostaria de participar, entre em contato comuigo pelo direct" sendo -u e -p email de login e senha do linkedin
python script.py post-comment -u <email> -p <password> -c "Gostaria de participar, entre em contato comuigo pelo direct"

```
## Configurações e variaveis de ambiente:
Por padrão o CLI exige que informe no comando o login e o email do usuário do linkedin o qual quer usar na automação, porém isso pode ser adicionado como variável de ambiente, assim como é visto no arquivo env-example
- LINKEDIN_EMAIL para seu email de usuário
- LINKEDIN_PASS para a senha do linkedin 
- DB_FILENAME para o arquivo do sqlite
- SE_ROUTER_HOST para o hostname do selenium grid
- SE_ROUTER_PORT para a porta do hsot do selenium grid

# Roadmap
Uma lista das coisas que não fiz e pretendo fazer:
## Melhorias em bot
- [] Implementar busca de postagem melhor
    - [] permitir buscar mais que os 10 primeiros posts
    - [] evitar postagens sem comentário na ação de comentário
- [] Implementar uma melhor network
    - [] Seguir autores
    - [] Enviar mensagem sobre postagem
        - [] Implementar estrutura de postagem de 
    - [] Conectar autor (conta premiun)
- [] Implementar estrutura de template de texto de comentário
## Melhorias de arquitetura
- [] Implementar arquitetura de eventos
    - [] Ao encontrar uma postagem
    - [] Ao comentar uma postagem
    - [] Ao seguir um autor
    - [] Ao se conectar a um autor
- [] Adicionar estrutura de execuçãoo fora do CLI usando eventos para iniciar processos
## Implementação de uma interface web
É sugerido a implementação usando Django + Django Rest Framework + Celery por ter um admin de graça e n precisar de um cliente (fullstack)
- [] sistema de usuários
- [] Base de dados de credenciais do linkedin
- [] Base de postagens encontradas
- [] Base de autores
    - Encontrados
    - Que sigo
    - Que adicionei
- [] Base de comentários feitos
- [] Base de mensagens enviadas
- [] Mudar para postgres (?)
- [] Escalonador de tarefas
    - [] Base de ações
        - [] Buscar posts com base em uma query
        - [] Comentar em postagens que não comentei antes
        - [] Seguir autores que ainda não sigo
        - [] Conectar a autores que ainda não sigo
        - [] Enviar mensageens a autores sobre postagens que ainda não mandei a mensagem + template de mensagem