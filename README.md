# Sua Grade UnB

O Sua Grade UnB é um projeto em desenvolvimento da matéria **Métodos de Desenvolvimento de Software**, a qual tem como objetivo auxiliar os alunos da Universidade de Brasília a montarem suas grades horárias de maneira fácil e intuitiva.

## ✨ Início

Você pode clonar o repositório do projeto com o seguinte comando:

```bash
git clone https://github.com/unb-mds/2023-2-Squad11.git
```

### Dependências globais

Para rodar o projeto, você precisa instalar as dependências globais, que são:

- GNU Make 4.3 (ou superior)
- Python v3.11.6 e Pip v22.0.2 (ou superior)
- Node v20.9.0 e NPM v10.1.0 (ou superior)
- Docker Engine v24.0.6 e Docker Compose v2.21.0 (ou superior)

### Ambiente

Para configurar o ambiente, você pode rodar o seguinte script:

```bash
make config
```

### Dependências do projeto

Para instalar as dependências do projeto, você pode rodar os seguintes comando:

```bash
# Crie um ambiente virtual Python
python3 -m venv env

# Ative o ambiente virtual
source env/bin/activate

# Instale os pacotes do Python e Node
make install
```

### Execução

Para executar o projeto, você pode rodar o seguinte comando:

```bash
docker compose up
```

**Observações do Docker:**

```bash
# Se você quiser rodar em segundo plano
docker compose up -d

# Se alterações foram feitas no Dockerfile ou no docker-compose.yml
docker compose up --build

# Se for necessário deletar os volumes
docker compose down -v
```

### Migrations

Para criar possíveis novas migrations, você pode rodar o seguinte comando:

```bash
python3 ./api/manage.py makemigrations --settings=core.settings.dev
```

## 📚 Documentação

A documentação do projeto pode ser encontrada clicando [aqui](https://unb-mds.github.io/2023-2-Squad11/).
