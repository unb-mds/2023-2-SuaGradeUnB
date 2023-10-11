# Definição de rotas

## Rotas do web site "Sua Grade UnB"

### Autenticação do Google

**Método HTTP:** `GET`
**Rota:** `/auth/google`

Essa rota permite ao usuário fazer login com sua conta do Google.

**Response:**

A resposta conterá informações de autenticação bem-sucedida, incluindo um token de autenticação.

```json
body: {   
    "access_token": "token_de_acesso"
}
```

- `"access_token"`: O token de acesso que permite ao usuário autenticado acessar recursos protegidos.

### Consulta da Grade de Matérias

**Método HTTP:** `GET`
**Rota:** `/schedules`

Após a seleção das matérias, o usuário pode acessar esta rota para visualizar a grade de matérias gerada pela API da faculdade.

**Requests:**

```json
headers = {
    "Authorization": "Token"
}
```

**Response:**

```json
{
    "schedules": {
        "id": 123,
        "name": "Grade 1",
        "date": "2021-01-01",
        "schedule": [
            {
                "day": "Segunda-feira",
                "courses": [
                    {
                        "name": "Cálculo 1",
                        "time": "2M34"
                    },
                    {
                        "name": "Fisica 1",
                        "time": "2T23"
                    }
                ]
            },
            {
                "day": "Terça-feira",
                "courses": [
                    {
                        "name": "Cálculo 1",
                        "time": "3M34"
                    },
                    {
                        "name": "Fisica 1",
                        "time": "3T23"
                    }
                ]
            }
        ]
    }
}
```

- `"schedule"`: Uma lista de objetos representando a grade de matérias por dia. Cada objeto possui um campo `"day"` e uma lista de cursos `"courses"` para esse dia.

### Visualização de Perfil

**Método HTTP:** `GET`
**Rota:** `/profile`

Esta rota permite ao usuário visualizar seu perfil, incluindo informações pessoais e configurações.

**Requests:**

```json
headers = {
    "Authorization": "Token"
}
```

**Response:**

```json
{   
    "info": {
        "foto": "link",
        "nome": "Nome do Usuário",
        "email": "email_do_cliente@example.com"
    }  
}
```

### Logout

**Método HTTP:** `GET`
**Rota:** `/logout`

Esta rota permite ao usuário fazer logout de sua conta no site.

**Requests:**

```json
headers = {
    "Authorization": "Token"
}
```

### Montagem de Grade

**Método HTTP:** `POST`
**Rota:** `/schedules/create`

Esta rota permite ao usuário realizar uma montagem de grade, selecionando especificamente as matérias e horários desejados.

**Response:**

```json
{
    "mode": "manual | automatic",
    "preference": "M",

    "courses": [
        {
            "name": "Tópicos Especiais em Engenharia de Software",
            "times": [
                ["23M34","Segunda e Terça - 10:00 a 12:00"],
                ["2T23","Segunda - 14:00 a 16:00"]
            ],
            "professors": ["BRUNO CESAR RIBAS", "EDSON ALVES DA COSTA JUNIOR"]
        },
        {
            "name": "Fisica 1",
            "times": [
                ["45M34","Quarta e Quinta - 10:00 a 12:00"],
                ["6T23","Sexta - 14:00 a 16:00"]
            ],
            "professors": ["LUIZA YOKO", "RAFAEL MORGADO DA SILVA"]

        }
    ]
}
```

- `"courses"`: Uma lista de objetos representando as matérias selecionadas manualmente. Cada objeto contém o `"name"` (nome da matéria), `"day"` (dia da semana) e `"time"` (horário).

- `"preference"`: A preferência de horário escolhida pelo usuário (por exemplo, "M" para manhã, "T" para tarde, "N" para noite).

- `"professors"`: Uma lista de nomes de professores preferidos escolhidos pelo usuário.

### Deleção de Grade Salva

**Método HTTP:** `DELETE`
**Rota:** `/schedules`

O usuário pode usar esta rota para excluir uma grade de matérias salva anteriormente, caso deseje remover uma configuração específica.

**Requests:**

```json
headers = {
    "Authorization": "Token"
}
```

**Response:**

```json
{
    "schedule_id": 123
}
```

- `"schedule_id"`: O identificador único da grade de matérias a ser excluída.
