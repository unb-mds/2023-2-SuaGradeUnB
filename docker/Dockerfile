FROM python:3.11.5-alpine3.18

# definir o diretório de trabalho
WORKDIR /usr/src/app

# definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# instalar dependências do poastgres
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# copiar os requisitos python
COPY ./requirements.txt /usr/src/app/requirements.txt

# instalação das dependências
RUN pip install --upgrade pip && \
    pip install -r /usr/src/app/requirements.txt

# copiar entrypoint.sh e dar permissão de execução
COPY ./docker/entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copiar o projeto
COPY ./api /usr/src/app/

# executar o arquivo de inicialização
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]