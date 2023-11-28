# [Sua Grade UnB](https://suagradeunb.com.br/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![codecov](https://codecov.io/gh/unb-mds/2023-2-Squad11/branch/main/graph/badge.svg?token=ZQZQZQZQZQ)](https://codecov.io/gh/unb-mds/2023-2-Squad11)
[![GitHub issues](https://img.shields.io/github/issues/unb-mds/2023-2-Squad11)]()
[![GitHub contributors](https://img.shields.io/github/contributors/unb-mds/2023-2-Squad11)]()
[![GitHub stars](https://img.shields.io/github/stars/unb-mds/2023-2-Squad11)]()
[![Hit Counter](https://views.whatilearened.today/views/github/unb-mds/2023-2-Squad11.svg)](https://views.whatilearened.today/views/github/unb-mds/2023-2-Squad11.svg)
</br>

[![Python version](https://img.shields.io/badge/python-3.11.6-blue)](https://www.python.org/downloads/release/python-3116/)
[![Django version](https://img.shields.io/badge/django-4.2.5-blue)](https://www.djangoproject.com/download/)
[![Node version](https://img.shields.io/badge/node-20.9.0-blue)](https://nodejs.org/en/download/)
[![npm version](https://img.shields.io/badge/npm-10.2.3-blue)](https://nodejs.org/en/download/)
[![Docker version](https://img.shields.io/badge/docker-24.0.7-blue)](https://docs.docker.com/engine/install/)
[![Docker Compose version](https://img.shields.io/badge/docker_compose-2.21.0-blue)](https://docs.docker.com/compose/install/)

O Sua Grade UnB é um projeto da matéria **Métodos de Desenvolvimento de Software**, a qual tem como objetivo auxiliar os alunos da Universidade de Brasília a montarem suas grades horárias de maneira fácil e intuitiva.

Com apenas alguns cliques, o aluno poderá montar sua grade horária de acordo com as matérias que deseja cursar. Além disso, o sistema auxiliará o aluno ao resolver os conflitos de horários entre as matérias escolhidas, retornando as melhores opções de horários de acordo com suas preferências.

O projeto é software livre e está sob a licença [MIT](./LICENSE).

## 📝 Sumário

- [Sua Grade UnB](#sua-grade-unb)
  - [📝 Sumário](#📝-sumário)
  - [👥 Equipe](#👥-equipe)
  - [✨ Início](#✨-início)
    - [📋 Pré-requisitos](#📋-pré-requisitos)
    - [💻 Ambiente](#💻-ambiente)
    - [📁 Dependências do projeto](#📁-dependências-do-projeto)
    - [💾 Execução](#💾-execução)
    - [✅ Autenticação do Google OAuth](#✅-autenticação-do-google-oauth)
    - [🖱️ Acesso aos serviços](#🖱️-acesso-aos-serviços)
    - [📍 Migrations](#📍-migrations)
  - [📚 Documentação](#📚-documentação)
  - [📎 Extra](#📎-extra)

## 👥 Equipe

| Nome | GitHub |
| :--- | :----: |
| Arthur Ribeiro e Sousa | [@artrsousa1](https://github.com/artrsousa1) |
| Caio Falcão Habibe Costa | [@CaioHabibe](https://github.com/CaioHabibe) |
| Caio Felipe Rocha Rodrigues| [@caio-felipee](https://github.com/caio-felipee) |
| Gabriel Henrique Castelo Costa | [@GabrielCastelo-31](https://github.com/GabrielCastelo-31) |
| Henrique Camelo Quenino | [@henriquecq](https://github.com/henriquecq) |
| Mateus Vieira Rocha da Silva | [@mateusvrs](https://github.com/mateusvrs) |

## ✨ Início

Você pode clonar o repositório do projeto com o seguinte comando:

```bash
git clone https://github.com/unb-mds/2023-2-Squad11.git
```

### 📋 Pré-requisitos

Para rodar o projeto, você precisa instalar as dependências globais, que são:

- GNU Make 4.3 (ou superior)
- Python v3.11.6 e Pip v22.0.2 (ou superior)
- Node v20.9.0 e NPM v10.1.0 (ou superior)
- Docker Engine v24.0.6 e Docker Compose v2.21.0 (ou superior)

### 💻 Ambiente

Para configurar o ambiente, você pode rodar o seguinte script:

```bash
make config
```

### 📁 Dependências do projeto

Para instalar as dependências do projeto, você pode rodar os seguintes comando:

```bash
# Crie um ambiente virtual Python
python3 -m venv env

# Ative o ambiente virtual
source env/bin/activate

# Instale os pacotes do Python e Node
make install
```

### 💾 Execução

Para executar o projeto, você pode rodar o seguinte comando:

```bash
docker compose up
```

#### Observações do Docker

```bash
# Se você quiser rodar em segundo plano
docker compose up -d

# Se alterações foram feitas no Dockerfile ou no docker-compose.yml
docker compose up --build

# Se for necessário deletar os volumes
docker compose down -v
```

### ✅ Autenticação do Google OAuth

Para que o login com o Google funcione, é necessário trocar o `your_client_id` no arquivo `web/.env.local` pelo **Client ID** do projeto no Google Cloud.

1. Crie um projeto no [Google Cloud](https://console.cloud.google.com/).
2. Vá para a página de [Credenciais](https://console.cloud.google.com/apis/credentials) do projeto.
3. Clique em **Criar credenciais** e selecione **ID do cliente OAuth**.
4. Selecione **Aplicativo da Web**.
5. Adicione `http://localhost:3000` como **Origens JavaScript autorizadas** e **URIs de redirecionamento autorizadas**.
6. Copie o **Client ID** e cole no arquivo `web/.env.local` no lugar de `your_client_id`.

Após isto:

1. Vá para a página de [OAuth Consent Screen](https://console.cloud.google.com/apis/credentials/consent).
2. Selecione **Usuários externos** e clique em **Criar**.
3. Preencha os campos obrigatórios e clique em **Salvar e continuar**.
4. Na seção **Usuários de Teste** adicione o seu e-mail e clique em **Adicionar**.
5. Clique em **Salvar e continuar**.

Adicionando serviços:

1. Entre na aba **APIs e Serviços**.
2. Clique em **Ativar APIs e Serviços**.
3. Ative os seguintes serviços:
    - IAM Service Account Credentials API
    - Identity and Access Management (IAM) API


### 🖱️ Acesso aos serviços

| Serviço | URL |
| :--- | :----: |
| Frontend | [http://localhost:3000](http://localhost:3000) |
| Backend | [http://localhost:8000](http://localhost:8000) |

### 📍 Migrations

Migration é um recurso do Django que permite que você altere o modelo de dados do seu projeto. Portanto, sempre que você alterar o modelo de dados, você deve criar uma nova migration.

Para criar possíveis novas migrations, você pode rodar o seguinte comando:

```bash
# Crie as migrations
make makemigrations

# Execute as migrations
make migrate
```

## 📚 Documentação

A documentação do projeto pode ser encontrada clicando [aqui](https://unb-mds.github.io/2023-2-Squad11/).

## 📎 Extra

### Story Map e Activity Flow

- Para acessar o Story Map e o Activity Flow, clique [aqui](https://miro.com/app/board/uXjVNYnku7s=/?share_link_id=596015837126).

### Arquitetura

- Para acessar a arquitetura do projeto, clique [aqui](https://www.figma.com/file/ZhAq8LRcclpWHYi4XnUySw/Sua-Grade-UnB---System-Design?type=whiteboard&node-id=0%3A1&t=k46HHNk4NotrkTpX-1).

### Protótipo

- Para acessar o protótipo do projeto, clique [aqui](https://www.figma.com/proto/o5Ffh1fWmmQz7KcDGuHrVP/Sua-grade-UNB?type=design&node-id=16-2775&scaling=scale-down&page-id=0%3A1&mode=design&t=L5JwoVdZsjyLBGdb-1).