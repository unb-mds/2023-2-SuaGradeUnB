---
hide:
  - navigation
--- 

# Definição de rotas

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec auctor, nisl eget ultricies ultricies, nunc nisl ultricies nunc, quis ul

## Autenticação do Google

**Método HTTP:** `POST` <br>
**Rota:** `/users/register`

Esta rota permite ao usuário fazer o login usando o Google OAuth2. Caso o usuário não tenha uma conta, uma nova será criada.

**Request:**

O request deve conter um token de autenticação do Google.

```js
body = {
    "access_token": "token"
}
```
- `"access_token"`: O token de acesso do Google OAuth2.

**Response:**

A resposta conterá informações de autenticação bem-sucedida, incluindo um token de autenticação.

**Success (200 OK)**

```js
headers = {
    "Content-Type": "application/json",
    "Set-Cookie": "refresh=<refresh-token>; Secure; HttpOnly; SameSite=Lax; Expires=<expires-date>"
},
body = {
    "access": "token",
    "first_name": "name",
    "last_name": "name",
    "email": "email"
}
```

**Error (400 BAD REQUEST)**

```js
body = {
    "errors": "descriptive error message"
}
```

## Login 

**Método HTTP:** `POST` <br>
**Rota:** `/users/login`

Esta rota atualiza o *refresh-token* do usuário e retorna um novo *access-token*.

**Request:**

O request deve conter um *refresh-token*.

```js
headers = {
    "Cookie": "refresh=<refresh-token>"
}
```

**Response:**

**Success (200 OK)**

```js
headers = {
    "Set-Cookie": "refresh=<refresh-token>; Secure; HttpOnly; SameSite=Lax; Expires=<expires-date>"
},
body = {
    "access": "token",
    "first_name": "name",
    "last_name": "name",
    "email": "email"
}
```

## Logout

**Método HTTP:** `POST` <br>
**Rota:** `users/logout`

Esta rota permite ao usuário fazer logout de sua conta no site.

**Request:**

```js
headers = {
    "Cookie": "refresh=<refresh-token>",
    "Authorization": "Bearer <access-token>"
}
```

**Response:**

**Suceess (200 OK)**

```js
body = {
    "message": "Successfully logged out."
}
```

**Error (400 BAD REQUEST)**

```js
body = {
    "errors": "descriptive error message"
}
```

**Error (401 UNAUTHORIZED)**

```js
body = {
    "errors": "access token not provided or invalid"
}
```

## Busca por Matéria

**Método HTTP:** `GET` <br>
**Rota:** `/courses/?search=<search>`

Esta rota permite ao usuário pesquisar e encontrar informações detalhadas sobre matérias potenciais que podem se relacionar com o termo de busca *(máximo 5)*. A busca deve ser pelo nome da matéria. 

**Response:**

A resposta incluirá informações detalhadas sobre as matérias potenciais que se relacionam com o termo de busca.

**Success (200 OK):**

```js
body = {
    "courses": [
        {
            "name": "Tópicos Especiais em Programação",
            "code": "FGA0053",
            "options": [
                {
                    "teachers": ["Edson Alves da Costa Junior"],
                    "schedule": "2M34",
                    "days": ["Segunda e Terça - 10:00 a 12:00"],
                    "classroom": "FGA - S1",
                    "workload": 60, 
                    "class": 1
                }
            ]
        }
    ]
}
```

**Error (400 BAD REQUEST):**

```js
body = {
    "errors": "descriptive error message"
}
```

## Montagem de Grade

**Método HTTP:** `POST` <br>
**Rota:** `/schedules/automatic/create`

Esta rota permite ao usuário criar uma grade de matérias, selecionando manualmente as matérias e horários ou deixando o sistema escolher automaticamente por preferencias determinadas pelo usuário. Ao utilizar esta rota, o usuário receberá três opções de grade.

**Request:**

```js
body = {
    "preference": "M|T|N", 
    "courses": [
        {
            "name": "Tópicos Especiais em Engenharia de Software",
            "code": "ESW101",
            "options": [
                {
                    "teachers": ["Edson Alves da Costa Junior"],
                    "schedule": "2M34"
                },
                {
                    "teachers": ["BRUNO CESAR RIBAS"],
                    "schedule": "2T23"
                }
            ]
        },
        {
            "name": "Fisica 1",
            "code": "FIS101"
        }
    ]
}
```

- Caso as opções de matéria possuam horários ou professores ou ambos, o sistema dará preferência para escolha dessas opções. Caso contrário, o sistema escolherá automaticamente.

**Response:**

**Success (200 OK):**

A resposta incluirá três opções de grade de matérias, com base nas preferências do usuário.

```js
body = {
    "schedules": [
        {
            "courses": [
                {
                    "FGA0053": {
                        "teachers": ["Edson Alves da Costa Junior"],
                        "schedule": "2M34"
                    },
                    "FGA0030": {
                        "teachers": ["BRUNO CESAR RIBAS"],
                        "schedule": "2T23"
                    }
                }
            ]
        },
        ...
    ]
}
```

**Error (400 BAD REQUEST):**

```js
body = {
    "errors": "descriptive error message"
}
```

## Salvar Grade

**Método HTTP:** `POST` <br>
**Rota:** `/schedules/save`

Esta rota permite ao usuário salvar uma grade de matérias, caso deseje utilizá-la novamente no futuro.

**Request:**

```js
header = {
    "Authorization": "Bearer <access-token>"
},
body = {
    "id": 123,
    "courses": [
        {
            "FGA0053": {
                "teachers": ["Edson Alves da Costa Junior"],
                "schedule": "2M34"
            },
            "FGA0030": {
                "teachers": ["BRUNO CESAR RIBAS"],
                "schedule": "2T23"
            }
        }
    ]
}
```

**Response:**

**Success (201 CREATED):**

A resposta confirmará a criação bem-sucedida da grade de matérias.

```js
body = {
    "message": "Grade salva com sucesso."
}
```

**Error (400 BAD REQUEST):**

```js
body = {
    "errors": "descriptive error message"
}
```

**Error (401 UNAUTHORIZED):**

```js
body = {
    "errors": "access token not provided or invalid"
}
```

## Consulta da Grade de Matérias

**Método HTTP:** `GET` <br>
**Rota:** `/schedules`

Esta rota permite ao usuário visualizar as grades de matérias criadas e salvas por ele.

**Request:**

```js
headers = {
    "Authorization": "Bearer <access-token>"
}
```

**Response:**

**Success (200 OK):**

A resposta incluirá uma lista de grades de matérias salvas pelo usuário.

```js
body = {
    "schedules": [
        {
            "id": 123,
            "courses": [
                {
                    "FGA0053": {
                        "teachers": ["Edson Alves da Costa Junior"],
                        "schedule": "2M34"
                    },
                    "FGA0030": {
                        "teachers": ["BRUNO CESAR RIBAS"],
                        "schedule": "2T23"
                    }
                }
            ]
        }
    ]
}
```

**Error (400 BAD REQUEST):**

```js
body = {
    "errors": "descriptive error message"
}
```

**Error (401 UNAUTHORIZED):**

```js
body = {
    "errors": "access token not provided or invalid"
}
```

## Deleção de Grade Salva

**Método HTTP:** `DELETE` <br>
**Rota:** `/schedules/delete`

Esta rota permite ao usuário excluir uma grade de matérias salva anteriormente.

**Request:**

```js
headers = {
    "Authorization": "Bearer <access-token>"
},
body = {
    "id": 123
}
```

**Response:**

**Success (200 OK):**

A resposta confirmará a exclusão bem-sucedida da grade de matérias.

```js
body = {
    "message": "Successfully deleted."
}
```

**Error (400 BAD REQUEST):**

```js
body = {
    "errors": "descriptive error message"
}
```

**Error (401 UNAUTHORIZED):**

```js
body = {
    "errors": "access token not provided or invalid"
}
```