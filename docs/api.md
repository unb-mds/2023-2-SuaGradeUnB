---
hide:
  - navigation
---

# Definição de rotas

Nesta seção, serão definidas as rotas da API, bem como os métodos HTTP e os parâmetros necessários para cada uma delas.

## Autenticação do Google

**Método HTTP:** `POST` <br>
**Rota:** `/users/register`

Esta rota permite ao usuário fazer o login usando o Google OAuth2. Caso o usuário não tenha uma conta, uma nova será criada.

**Request:**

O request deve conter um token de autenticação do Google.

```js linenums="1"
body = {
  access_token: "token",
};
```

- `"access_token"`: O token de acesso do Google OAuth2.

**Response:**

A resposta conterá informações de autenticação bem-sucedida, incluindo um token de autenticação.

**Success (200 OK)**

```js linenums="1"
(headers = {
  "Content-Type": "application/json",
  "Set-Cookie":
    "refresh=<refresh-token>; Secure; HttpOnly; SameSite=Lax; Expires=<expires-date>",
}),
  (body = {
    access: "token",
    first_name: "name",
    last_name: "name",
    email: "email",
    picture_url: "picture_url",
  });
```

**Error (400 BAD REQUEST)**

```js linenums="1"
body = {
  errors: "descriptive error message",
};
```

## Login

**Método HTTP:** `POST` <br>
**Rota:** `/users/login`

Esta rota atualiza o _refresh-token_ do usuário e retorna um novo _access-token_.

**Request:**

O request deve conter um _refresh-token_.

```js linenums="1"
headers = {
  Cookie: "refresh=<refresh-token>",
};
```

**Response:**

**Success (200 OK)**

```js linenums="1"
(headers = {
  "Set-Cookie":
    "refresh=<refresh-token>; Secure; HttpOnly; SameSite=Lax; Expires=<expires-date>",
}),
  (body = {
    access: "token",
    first_name: "name",
    last_name: "name",
    email: "email",
    picture_url: "picture_url",
  });
```

## Logout

**Método HTTP:** `POST` <br>
**Rota:** `users/logout`

Esta rota permite ao usuário fazer logout de sua conta no site.

**Request:**

```js linenums="1"
headers = {
  Cookie: "refresh=<refresh-token>",
};
```

**Response:**

**Suceess (200 OK)**

**Error (400 BAD REQUEST)**

**Error (401 UNAUTHORIZED)**

**OBSERVAÇÃO:** As respostas não contém conteúdo.

## Busca por Matéria

**Método HTTP:** `GET` <br>
**Rota:** `/courses/?search=<search>&year=<year>&period=<period>`

Esta rota permite ao usuário pesquisar e encontrar informações detalhadas sobre matérias potenciais que podem se relacionar com o termo de busca _(máximo 8)_. A busca deve ser pelo nome ou código da disciplina.

**Response:**

A resposta incluirá informações detalhadas sobre as matérias potenciais que se relacionam com o termo de busca.

**Success (200 OK):**

```js linenums="1"
body = [
  {
    id: 20696,
    department: {
      id: 962,
      code: "673",
      year: "2023",
      period: "2",
    },
    classes: [
      {
        id: 91560,
        teachers: ["EDSON ALVES DA COSTA JUNIOR"],
        classroom: "FGA - I6",
        schedule: "35T6 35N1",
        days: ["Terça-feira 18:00 às 19:50", "Quinta-feira 18:00 às 19:50"],
        _class: "01",
        special_dates: [],
        discipline: 20696,
      },
      {
        id: 91561,
        teachers: ["EDSON ALVES DA COSTA JUNIOR"],
        classroom: "FGA - MOCAP",
        schedule: "6T2345",
        days: ["Sexta-feira 14:00 às 17:50"],
        _class: "02",
        special_dates: [],
        discipline: 20696,
      },
    ],
    name: "TÓPICOS ESPECIAIS EM PROGRAMAÇÃO",
    code: "FGA0053",
  },
];
```

**Error (400 BAD REQUEST):**

```js linenums="1"
body = {
  errors: "no valid argument found for 'search', 'year' or 'period'",
};
```

ou

```js linenums="1"
body = {
  errors: "search must have at least 4 characters",
};
```

## Montagem de Grade

**Método HTTP:** `POST` <br>
**Rota:** `/courses/schedule`

Esta rota permite ao usuário criar uma grade de matérias deixando o sistema escolher automaticamente por preferencias determinadas pelo usuário. Ao utilizar esta rota, o usuário receberá três opções de grade.

**Request:**

```js linenums="1"
body = {
  preference: "M|T|N",
  classes: [ class_id: int, ... ]
};
```

- O campo _classes_ recebe um array de inteiros contendo os ids das turmas selecionadas.

**Response:**

**Success (200 OK):**

A resposta incluirá três opções de grade de matérias, com base nas preferências do usuário.

```js linenums="1"
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

```js linenums="1"
body = {
  errors: "descriptive error message",
};
```

## Salvar Grade

**Método HTTP:** `POST` <br>
**Rota:** `/courses/schedules/save`

Esta rota permite ao usuário salvar uma grade de matérias, caso deseje utilizá-la novamente no futuro.

**Request:**

```js linenums="1"
(header = {
  Authorization: "Bearer <access-token>",
}),
  (body = [
    [
      {
        FGA0053: {
          teachers: ["Edson Alves da Costa Junior"],
          schedule: "2M34",
        },
        FGA0030: {
          teachers: ["BRUNO CESAR RIBAS"],
          schedule: "2T23",
        },
      },
    ], ...
  ]);
```

**Response:**

**Success (201 CREATED):**

A resposta confirmará a criação bem-sucedida da grade de matérias.

```js linenums="1"
body = {
  message: "Grade salva com sucesso.",
};
```

**Error (400 BAD REQUEST):**

```js linenums="1"
body = {
  errors: "descriptive error message",
};
```

**Error (401 UNAUTHORIZED):**

```js linenums="1"
body = {
  errors: "access token not provided or invalid",
};
```

## Consulta da Grade de Matérias

**Método HTTP:** `GET` <br>
**Rota:** `/courses/schedules`

Esta rota permite ao usuário visualizar as grades de matérias criadas e salvas por ele.

**Request:**

```js linenums="1"
headers = {
  Authorization: "Bearer <access-token>",
};
```

**Response:**

**Success (200 OK):**

A resposta incluirá uma lista de grades de matérias salvas pelo usuário.

```js linenums="1"
body = {
  schedules: [
    {
      id: 123,
      courses: [
        {
          FGA0053: {
            teachers: ["Edson Alves da Costa Junior"],
            schedule: "2M34",
          },
          FGA0030: {
            teachers: ["BRUNO CESAR RIBAS"],
            schedule: "2T23",
          },
        },
      ],
    },
  ],
};
```

**Error (400 BAD REQUEST):**

```js linenums="1"
body = {
  errors: "descriptive error message",
};
```

**Error (401 UNAUTHORIZED):**

```js linenums="1"
body = {
  errors: "access token not provided or invalid",
};
```

## Deleção de Grade Salva

**Método HTTP:** `DELETE` <br>
**Rota:** `/courses/schedules`

Esta rota permite ao usuário excluir uma grade de matérias salva anteriormente.

**Request:**

```js linenums="1"
(headers = {
  Authorization: "Bearer <access-token>",
}),
  (body = {
    id: 123,
  });
```

**Response:**

**Success (200 OK):**

A resposta confirmará a exclusão bem-sucedida da grade de matérias.

```js linenums="1"
body = {
  message: "Successfully deleted.",
};
```

**Error (400 BAD REQUEST):**

```js linenums="1"
body = {
  errors: "descriptive error message",
};
```

**Error (401 UNAUTHORIZED):**

```js linenums="1"
body = {
  errors: "access token not provided or invalid",
};
```
