---
hide:
  - navigation
---

# Como executar o projeto?

## ✨ Início

Você pode clonar o repositório do projeto com o seguinte comando:

```bash
git clone https://github.com/unb-mds/2023-2-SuaGradeUnB.git
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
python3 -m venv api/env

# Ative o ambiente virtual
source api/env/bin/activate

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

| Serviço  |                      URL                       |
| :------- | :--------------------------------------------: |
| Frontend | [http://localhost:3000](http://localhost:3000) |
| Backend  | [http://localhost:8000](http://localhost:8000) |

### 📍 Migrations

Migration é um recurso do Django que permite que você altere o modelo de dados do seu projeto. Portanto, sempre que você alterar o modelo de dados, você deve criar uma nova migration.

Para criar possíveis novas migrations, você pode rodar o seguinte comando:

```bash
# Crie as migrations
make makemigrations

# Execute as migrations
make migrate
```
