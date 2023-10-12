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

Esta rota permite ao usuário visualizar uma grade de matérias criada.


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
- `"courses"`: Uma lista de objetos representando as matérias selecionadas manualmente. Cada objeto contém o `"name"` (nome da matéria) e `"time"` (horário).
- `"date"`: A data em que a grade de matérias foi criada.
- `"name"`: O nome da grade da matéria.
- `"id"`: O identificador único da grade de matérias.
- `"day"`: O dia da semana em que é ministrada a aula.
- `"time"`: Código que fornece o horário em que é ministrada a aula e bem o dia da semana em que acontece.


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

Esta rota permite ao usuário criar uma grade de matérias, selecionando manualmente as matérias e horários ou deixando o sistema escolher automaticamente por preferencias determinadas pelo usuário.

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
- `"mode"`: O modo de montagem da grade de matérias, que pode ser manual ou automático.
- `"schedule"`: Uma lista de objetos representando a grade de matérias por dia. Cada objeto possui um campo `"day"` e uma lista de cursos `"courses"` para esse dia.
- `"courses"`: Uma lista de objetos representando as matérias selecionadas manualmente. Cada objeto contém o `"name"` (nome da matéria) e `"time"` (horário).


### Update de Grade 

**Método HTTP:** `PUT` Rota: `/schedules/update`

Esta rota permite ao usuário atualizar uma grade de matérias salva anteriormente, caso deseje alterar uma configuração específica.

**Requests:**

```json
headers = {
    "Authorization": "Token"
}
```
**Response:**
```json
body: {
    "schedule_id": 123,
    "mode": "manual",

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
- `"schedule_id"`: O identificador único da grade de matérias a ser atualizada.
- `"courses"`: Uma lista de objetos representando as matérias selecionadas manualmente. Cada objeto contém o `"name"` (nome da matéria), `"day"` (dia da semana) e `"time"` (horário).
- `"professors"`: Uma lista de nomes de professores preferidos escolhidos pelo usuário.

**Response:**

A resposta confirmará a atualização bem-sucedida da grade de matérias.

```json
{
    "message": "Grade atualizada com sucesso."
}
```

## Busca por Matéria

**Método HTTP:** `GET`
**Rota:** `/courses/search`

Esta rota permite ao usuário pesquisar e encontrar informações detalhadas sobre uma matéria específica na universidade.

**Request:**

```json
query = "Cálculo 1"
```

- `query`: A consulta que o usuário deseja fazer para encontrar informações sobre uma matéria específica.

**Response:**

A resposta incluirá informações detalhadas sobre a matéria procurada.

```json
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
