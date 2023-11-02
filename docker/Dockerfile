FROM python:3.11.6-alpine3.18

# definir o diretório de trabalho
WORKDIR /usr/src/api

# definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# instalar dependências do poastgres
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# copiar os requisitos python
COPY ./requirements.txt /usr/src/api/requirements.txt

# instalação das dependências
RUN pip install --upgrade pip && \
    pip install -r /usr/src/api/requirements.txt

# copiar entrypoint.sh e dar permissão de execução
COPY ./api/entrypoint.sh /usr/src/api/entrypoint.sh
RUN chmod +x /usr/src/api/entrypoint.sh

# copiar o projeto
COPY ./api /usr/src/api/

# executar o arquivo de inicialização
ENTRYPOINT ["/usr/src/api/entrypoint.sh"]