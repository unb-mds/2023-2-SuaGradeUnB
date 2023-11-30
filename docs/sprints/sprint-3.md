# Sprint 3

Período: 27/09/2023 a 04/10/2023

## Descrição

Nessa _Sprint_ o grupo definiu e criou o [protótipo](https://www.figma.com/file/ZhAq8LRcclpWHYi4XnUySw/Sua-Grade-UnB---System-Design?type=whiteboard&node-id=0%3A1&t=cMpcdtmFllfPV9Xq-1) da arquitetura do projeto. Além disso, para o time do back-end, foi definido como _task_ procurar e estudar as bibliotecas necessárias para _web-scraping_ e montagem de grade.

Para o time DevOps, o objetivo da semana foi a comunicação com a administradora da organização para instalar o app _Codecov_ no repositório do projeto.

## Objetivos

- Definir e criar o protótipo da arquitetura do projeto
- Definir bibliotecas para _web-scraping_ e montagem de grade
- Comunicação com a administradora da organização para instalar o app _Codecov_ no repositório do projeto

## Reuniões

### Reunião 1

Data: 04/10/2023

Local: Gather Town

**Ata:**

Nessa reunião, o time _DevOps_ e _Back-end_ apresentou o protótipo da arquitetura do projeto e o time de back-end apresentou as bibliotecas escolhidas para _web-scraping_ e montagem de grade. Além disso, o time decidiu, juntamente com a professora que não haverá desenvolvimento mobile, portanto, o projeto é apenas web, ou seja, o _Front-end_ irá utilizar o _Next.js_ para o desenvolvimento, e no lugar do _Amazon SQS_ para fila e do _EC2 AWS_ para deploy vamos utilizar o _Redis_ com _Heroku_ para subir o referido site. Logo, nossa arquitetura ficou da seguinte forma:

- Design: Figma
- Framework: Next.js
- API:
    - Python:
        - Django
        - Django REST Framework
- Banco de dados: PostgreSQL
- Message Queue:
    - Celery
    - Redis
- DevOps:
    - Docker
    - CI/CD GitHub
    - Codecov
- Servidor:
    - Heroku

## Finalização

O time de DevOps não conseguiu finalizar a implementação do Codecov no GitHub Workflow, visto que era necessário o token do _Codecov_ para a configuração do aplicativo do Codecov no repositório do projeto.

---

**Observações:**

Para a próxima _Sprint_ o time de DevOps entrará em contato com os proprietários da organização [@unb-mds](https://github.com/unb-mds), para que seja fornecido o token do _Codecov_.
