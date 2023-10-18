# Definição de rotas

## Rotas do web site "Sua Grade UnB"

### Autenticação do Google

**Método HTTP:** `GET`
**Rota:** `/auth/google`

Essa rota permite ao usuário fazer login com sua conta do Google.

**Response:**

A resposta conterá informações de autenticação bem-sucedida, incluindo um token de autenticação.

```js
{
  "routes": [
    {
      "path": "/auth/google",
      "method": "GET",
      "description": "Iniciar autenticação do Google OAuth2.",
      "scope": ["profile", "email"]
    },
    {
      "path": "/auth/google/callback",
      "method": "GET",
      "description": "Rota de retorno de chamada após a autenticação do Google OAuth2. Recebe o token de acesso do Google.",
      "successRedirect": "/profile",
      "failureRedirect": "/login",
      "receivesAccessToken": true
    },
  ],
}

```

- `"access_token"`: O token de acesso que permite ao usuário autenticado acessar recursos protegidos.

### Consulta da Grade de Matérias

**Método HTTP:** `GET`
**Rota:** `/schedules`

Esta rota permite ao usuário visualizar várias grades de matérias criadas.

**Requests:**

```js
headers = {
    "Authorization": "Token"
}
```

**Response:**

```js
{
    "schedule 1": {
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
                        "code": "MAT101"
                        "teacher": ["LUIZA YOKO"]
                        "classroom": "S1"
                    },
                    {
                        "name": "Fisica 1",
                        "time": "2T23"
                        "code": "FIS101"
                        "teacher": ["RAFAEL MORGADO DA SILVA"]
                        "classroom": "S2"
                    }
                ]
            },
            {
                "day": "Terça-feira",
                "courses": [
                    {
                        "name": "Cálculo 1",
                        "time": "3M34"
                        "code": "MAT101"
                        "teacher": ["LUIZA YOKO"]
                        "classroom": "S1"
                    },
                    {
                        "name": "Fisica 1",
                        "time": "3T23"
                        "code": "FIS101"
                        "teacher": ["RAFAEL MORGADO DA SILVA"]
                        "classroom": "S2"
                    }
                ]
            }
        ]
    }
    "schedule 2": {
        "id": 456,
        "name": "Grade 2",
        "date": "2021-01-01",
        "schedule": [
            {
                "day": "Quarta-feira",
                "courses": [
                    {
                        "name": "Cálculo 1",
                        "time": "2M34"
                        "code": "MAT102"
                        "teacher": ["Ricardo Fragelli"]
                        "classroom": "S1"
                    },
                    {
                        "name": "Fisica 1",
                        "time": "2T23"
                        "code": "FIS104"
                        "teacher": ["RAFAEL MORGADO DA SILVA"]
                        "classroom": "S2"
                    }
                ]
            },
            {
                "day": "Sexta-feira",
                "courses": [
                    {
                        "name": "Cálculo 1",
                        "time": "3M34"
                        "code": "MAT102"
                        "teacher": ["Ricardo Fragelli"]
                        "classroom": "S1"
                    },
                    {
                        "name": "Fisica 1",
                        "time": "3T23"
                        "code": "FIS104"
                        "teacher": ["RAFAEL MORGADO DA SILVA"]
                        "classroom": "S2"
                    }
                ]
            }
        ]
    }
}
```

- `"schedule"`: Uma lista de objetos representando a grade de matérias por dia. Cada objeto possui um campo `"day"` e uma lista de cursos `"courses"` para esse dia.
- `"courses"`: Uma lista de objetos representando as matérias selecionadas manualmente. Cada objeto contém o `"name"` (nome da matéria), `"time"` (horário) e `"teacher"` (professor) e `"classroom"` (sala de aula).
- `"date"`: A data em que a grade de matérias foi criada.
- `"name"`: O nome da grade da matéria.
- `"id"`: O identificador único da grade de matérias.
- `"day"`: O dia da semana em que é ministrada a aula.
- `"time"`: Código que fornece o horário em que é ministrada a aula e bem o dia da semana em que acontece.
- `"teacher"`: O nome do professor que ministra a aula.
- `"classroom"`: O código da sala de aula em que é ministrada a aula.


### Visualização de Perfil

**Método HTTP:** `GET`
**Rota:** `/profile`

Esta rota permite ao usuário visualizar seu perfil, incluindo informações pessoais e configurações.

**Requests:**

```js
headers = {
    "Authorization": "Token"
}
```

**Response:**

```js
{   
    "info": {
        "photo": "link",
        "name": "Client name",
        "email": "client@email.com"
    }  
}
```
- `"photo"`: A foto de perfil do usuário.
- `"name"`: O nome do usuário.
- `"email"`: O email do usuário.

### Logout

**Método HTTP:** `GET`
**Rota:** `/logout`

Esta rota permite ao usuário fazer logout de sua conta no site.

**Requests:**

```js
headers = {
    "Authorization": "Token"
}
```

### Montagem de Grade

**Método HTTP:** `POST`
**Rota:** `/schedules/create`

Esta rota permite ao usuário criar uma grade de matérias, selecionando manualmente as matérias e horários ou deixando o sistema escolher automaticamente por preferencias determinadas pelo usuário.

**Response:**

```js
{
    "mode": "manual | automatic",
    "preference": "M",

    "courses": [
        {
            "name": "Tópicos Especiais em Engenharia de Software",
            "code": "ESW101",
            "times": [
                ["23M34","Segunda e Terça - 10:00 a 12:00"],
                ["2T23","Segunda - 14:00 a 16:00"]
            ],
            "professors": ["BRUNO CESAR RIBAS", "EDSON ALVES DA COSTA JUNIOR"]
        },
        {
            "name": "Fisica 1",
            "code": "FIS101",
            "times": [
                ["45M34","Quarta e Quinta - 10:00 a 12:00"],
                ["6T23","Sexta - 14:00 a 16:00"]
            ],
            "professors": ["LUIZA YOKO", "RAFAEL MORGADO DA SILVA"]

        }
    ]
}
```
- `"mode"`: O modo de montagem da grade de matérias, que pode ser manual ou automático.
- `"preference"`: A preferência de horário escolhida pelo usuário (por exemplo, "M" para manhã, "T" para tarde, "N" para noite).
- `"courses"`: Uma lista de objetos representando as matérias selecionadas manualmente. Cada objeto contém o `"name"` (nome da matéria), `"code"` (código da disciplina), `"day"` (dia da semana) e `"time"` (horário).
- `"name"`: O nome da matéria.
- `"code"`: O código da matéria na universidade.
- `"times"`: Uma lista de horários em que a matéria é ministrada.
- `"professors"`: Uma lista de nomes de professores preferidos escolhidos pelo usuário.

### Update de Grade 

**Método HTTP:** `PUT` Rota: `/schedules/update`

Esta rota permite ao usuário atualizar uma grade de matérias salva anteriormente, caso deseje alterar uma configuração específica.

**Requests:**

```js
headers = {
    "Authorization": "Token"
}
```
**Response:**
```js
body: {
    "schedule_id": 123,
    "mode": "manual",

    "courses": [
        {
            "name": "Tópicos Especiais em Engenharia de Software",
            "code": "ESW101",
            "times": [
                ["23M34","Segunda e Terça - 10:00 a 12:00"],
                ["2T23","Segunda - 14:00 a 16:00"]
            ],
            "professors": ["BRUNO CESAR RIBAS", "EDSON ALVES DA COSTA JUNIOR"]
        },
        {
            "name": "Fisica 1",
            "code": "FIS101",
            "times": [
                ["45M34","Quarta e Quinta - 10:00 a 12:00"],
                ["6T23","Sexta - 14:00 a 16:00"]
            ],
            "professors": ["LUIZA YOKO", "RAFAEL MORGADO DA SILVA"]

        }
    ]
}
```
- `"schedule_id"`: O identificador único da grade de matérias a ser atualizada.
- `"courses"`: Uma lista de objetos representando as matérias selecionadas manualmente. Cada objeto contém o `"name"` (nome da matéria), `"code"` (código da disciplina), `"day"` (dia da semana) e `"time"` (horário).

**Response:**

A resposta confirmará a atualização bem-sucedida da grade de matérias.

```js
{
    "message": "Grade atualizada com sucesso."
}
```

## Busca por Matéria

**Método HTTP:** `GET`
**Rota:** `/courses/search`

Esta rota permite ao usuário pesquisar e encontrar informações detalhadas sobre uma matéria específica na universidade.

**Request:**

```js
query = "Cálculo 1"
```

- `query`: A consulta que o usuário deseja fazer para encontrar informações sobre uma matéria específica.

**Response:**

A resposta incluirá informações detalhadas sobre a matéria procurada.

```js
{
    "course_name": "Cálculo 1",
    "course_code": "MAT101",
    "description": "Este curso aborda os conceitos fundamentais de cálculo, incluindo limites, derivadas e integrais.",
    "professors": ["LUIZA YOKO", "RICARDO FRAGELLI"],
    "schedule": [
        {
            "day": "Segunda-feira",
            "time": "2M34"
        },
        {
            "day": "Terça-feira",
            "time": "2T23"
        }
    ]
}
```

- `"course_name"`: O nome da matéria pesquisada.

- `"course_code"`: O código da matéria na universidade.

- `"description"`: Uma breve descrição do conteúdo do curso.

- `"professors"`: Uma lista de professores que ministram o curso.

- `"schedule"`: Um horário típico de aulas para a matéria, incluindo os dias da semana e horários.
### Deleção de Grade Salva

**Método HTTP:** `DELETE`
**Rota:** `/schedules`

O usuário pode usar esta rota para excluir uma grade de matérias salva anteriormente, caso deseje remover uma configuração específica.

**Requests:**

```js
headers = {
    "Authorization": "Token"
}
```

**Response:**

```js
{
    "schedule_id": 123
}
```

- `"schedule_id"`: O identificador único da grade de matérias a ser excluída.
