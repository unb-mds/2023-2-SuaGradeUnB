FROM python:3.11.5-alpine3.18

# definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# definir o diretório de trabalho
RUN mkdir /app
WORKDIR /app

# instalar os requisitos
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# copiar o conteúdo do diretório atual para o diretório de trabalho
COPY . /app/

# copiar e executar o arquivo de inicialização
COPY ./docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]