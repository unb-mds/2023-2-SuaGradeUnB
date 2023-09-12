# Sprint 0

Período: 04/09/2023 a 11/09/2023

## Descrição

Nessa _Sprint_ o time definiu que as reuniões semanais serão realizadas às segundas-feiras às 20:30 no Gather Town. Além disso, foi acordado que os 3 primeiros coelhos da semana serão responsáveis por estudar os conceitos básicos necessários para o desenvolvimento do projeto. Por fim, definimos qual será o tema da aplicação, os requisitos iniciais e os objetivos a serem alcançados, além de brevemente descrever quais serão as tecnologias utilizadas.

## Objetivos

- Definição dos horários das reuniões semanais
- Estudar Git e GitHub
- Estudar GitHub Flow
- Estudar Metodologias Ágeis
- Definir tema da aplicação
- Definir requisitos iniciais
- Definir tecnologias utilizadas

## Reuniões

### Reunião 1

Data: 04/09/2023

Local: Discord

**Ata:**

Nessa reunião, o time definiu os 3 primeiros coelhos da semana, que serão responsáveis por estudar os conceitos básicos necessários para o desenvolvimento do projeto:

- Git e GitHub ([Gabriel](https://github.com/GabrielCastelo-31))
- GitHub Flow ([Arthur](https://github.com/artrsousa1))
- Metodologias Ágeis ([Caio Felipe](https://github.com/caio-felipee))

### Reunião 2

Data: 08/09/2023

Local: Gather Town

**Ata:**

Na segunda reunião da _Sprint_, o time definiu que as reuniões semanais serão realizadas às segundas-feiras às 20:30 no Gather Town. Ademais, definimos que o tema da aplicação será a facilitação da criação de grades horárias pelos estudantes da UnB. Nisso, definimos os seguintes requisitos iniciais:

**Funcionais:**  

- Cadastro de usuário
    - Login por gmail
- Ler dados do SIGAA (Web scraping)
    - Filtrar dados necessários
    - Alocar dados no banco de dados próprio
- Apresentar dados para escolha do usuário
- Seleção do tipo de montagem:
    - Montagem manual
    - Automática:
        - Preferência de horário (Manhã, Tarde, Noite)
        - Preferência de professor
- Realizar montagem com base na escolha
- Salvamento de grades (Nuvem)
    - Permitir deleção das grades salvas.

**Não funcionais:**

- Portabilidade:
    - Mobile:
        - Android
        - IOS
    - Desktop
- Segurança (Google)
- Usabilidade:
    - Grade formato de texto (Pessoas com deficiência visual)
- Disponibilidade: 24/7
- Escalabilidade:
    - Utilização fluida para 5% da UnB
    - Tempo de resposta: 0.50s

Por fim, definimos as tecnologias que serão utilizadas e os setores que cada membro do time irá atuar:

**Arquitetura:**

- Design: Figma

- Framework: Flutter
- Micro-serviços (API):
    - Python:
        - Django
        - Django REST Framework
- Banco de dados: Amazon RDS PostgreSQL
- Message Queue:
    - Celery
    - Amazon SQS
- DevOps:
    - Docker + Kubernetes
    - CI/CD GitHub
    - Codecov
- Servidor:
    - EC2 AWS
  
**Setores:**

- Mobile + Design:
    - Arthur Ribeiro
    - Caio Habibe
- Back-end (API):
    - Gabriel Castelo
    - Henrique Quenino
- DevOps:
    - Caio Felipe
    - Mateus Vieira

## Finalização

O time conseguiu realizar todos os objetivos propostos para a _Sprint_.

---

**Observações:**

- Durante a segunda reunião o time descobriu o [Gather Town](https://gather.town/), uma plataforma que simula um ambiente físico e permite que os usuários se movimentem e interajam com outros usuários. Assim, a plataforma será utilizada para a realização das reuniões semanais do time.
