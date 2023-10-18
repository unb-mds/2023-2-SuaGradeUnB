# Sua Grade UnB

O Sua Grade UnB é um projeto em desenvolvimento da matéria **Métodos de Desenvolvimento de Software**, a qual tem como objetivo auxiliar os alunos da Universidade de Brasília a montarem suas grades horárias de maneira fácil e intuitiva.

## ✨ Início

Você pode clonar o repositório do projeto com o seguinte comando:

```bash
git clone https://github.com/unb-mds/2023-2-Squad11.git
```

### Dependências globais

Para rodar o projeto, você precisa instalar as dependências globais, que são:

- Python v3.11 (ou superior)
- Docker Engine v24.0.6 e Docker Compose v2.21.0 (ou superior)

### Ambiente

Para configurar o ambiente, você pode rodar o seguinte script:

```bash
bash ./scripts/env.sh
```

### Execução

Para executar o projeto, você pode rodar o seguinte comando:

```bash
docker compose up
```

### Migrations

Para criar possíveis novas migrations, você pode rodar o seguinte comando:

```bash
python3 ./api/manage.py makemigrations --settings=core.settings.dev
```

## 📚 Documentação

A documentação do projeto pode ser encontrada clicando [aqui](https://unb-mds.github.io/2023-2-Squad11/).
