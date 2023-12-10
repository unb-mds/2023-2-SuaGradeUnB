---
hide:
  - navigation
---

# Arquitetura

## Visão Geral

A arquitetura do sistema é composta por 2 aplicações: o [backend](https://api.suagradeunb.com.br) e o [frontend](https://suagradeunb.com.br). O backend é responsável por fornecer uma API REST que apresenta as seguintes funcionalidades:

- Usuários:
    - Autenticação
    - Armazenamento de grades salvas
- Disciplinas:
    - Busca por nome e código
- Grade:
    - Gerador de grade de horários

O frontend é responsável por consumir a API REST e apresentar as informações para o usuário final. O fluxo da aplicação se dá da seguinte forma:

1. O usuário acessa o site do [Sua Grade UnB](https://suagradeunb.com.br)
2. Há uma busca de disciplinas por nome ou código
3. O usuário seleciona as disciplinas que deseja cursar
4. O usuário gera as grades possíveis
5. O usuário salva a grade que desejar ou mantém no armazenamento local

## Design do Sistema

O design do sistema foi feito utilizando a ferramenta [Figma](https://www.figma.com) e comporta-se da seguinte forma:

1. O usuário acessa o site do [Sua Grade UnB](https://suagradeunb.com.br) e é apresentado com a tela de login
2. O usuário pode se cadastrar ou logar com uma conta já existente da Google
3. Há o redirecionamento para tela de login da Google
4. Logo após o login, a aplicação recebe um token de autenticação e a API pega as informações cedidas pela Google
5. Assim, há o redirecionamento para a tela de busca de disciplinas
6. O usuário pode buscar por disciplinas por nome ou código e a API gerencia esse _search_
7. O usuário pode selecionar as disciplinas que deseja cursar
8. Após isso, há um _request_ para gerar as grades possíveis e API retorna as 5 melhores grades
9. O usuário pode salvar a grade que desejar ou manter no armazenamento local
10. O salvamento é feito no Banco de Dados e a API gerencia esse _save_ para acessar posteriormente de qualquer dispositivo

### Lógica do WebScraping

Para nossa aplicação gerenciar as disciplinas e horários disponíveis, foi necessário fazer um _web scraping_ no site da [UnB](https://sigaa.unb.br/sigaa/public/turmas/listar.jsf) para obter as informações necessárias e não gerar um overload de requisições no site da universidade.

Após a obtenção dos dados, foi feito um tratamento para que as informações ficassem mais legíveis e organizadas para o usuário final, cadastrando-as no Banco de Dados PostgreSQL que é gerenciado pela API Django.

As requisições de web scraping ainda não são feitas de forma automática, mas sim pela equipe de desenvolvimento, assim tentamos executar o _web scraping_ a cada 24h para manter as informações atualizadas.

- Para execução do _web scraping_ de forma total é necessário executar o comando `make updatedb-all` no servidor da Heroku.

<div style="text-align:center;">
  <iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450" src="https://www.figma.com/embed?embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Ffile%2FZhAq8LRcclpWHYi4XnUySw%2FSua-Grade-UnB---System-Design%3Ftype%3Dwhiteboard%26node-id%3D0%253A1%26t%3Dlk1PjgzQ3UxvdktM-1" allowfullscreen></iframe>
</div>

### Lógica da criação de grades

Para a criação de grades, foi necessário utilizar o algoritmo de produto cartesiano para gerar todas as combinações possíveis de horários e disciplinas. Após isso, foi feito um tratamento para que as grades geradas não tivessem conflitos de horários e que não houvesse disciplinas repetidas.

- Para execução desse algoritmo foi utilizado o [itertools.product](https://docs.python.org/3/library/itertools.html#itertools.product) do Python.

**Extra:** Se você quiser saber mais sobre o algoritmo de produto cartesiano, pode acessar site [www.cuemath.com](https://www.cuemath.com/algebra/cartesian-product/).

## Tecnologias Utilizadas

- [Docker](https://www.docker.com)
- [Docker Compose](https://docs.docker.com/compose)

### Backend

- [Python](https://www.python.org)
- [Django](https://www.djangoproject.com)
- [Django REST Framework](https://www.django-rest-framework.org)
- [PostgreSQL](https://www.postgresql.org)
- [Heroku](https://www.heroku.com)

### Frontend

- [TypeScript](https://www.typescriptlang.org)
- [Next.js](https://nextjs.org)
- [Tailwind CSS](https://tailwindcss.com)
- [Vercel](https://vercel.com)
