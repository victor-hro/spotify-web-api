# Usa a imagem base do Python
FROM python:3.10


# Configura o diretório de trabalho no contêiner
WORKDIR /app

ENV OPENAI_API_KEY='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'

# Copia o código fonte para o contêiner
COPY src/app /app

# Copia o arquivo requirements.txt para o contêiner
COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

# Instala as dependências do Python
RUN pip install -r /app/requirements.txt

# Copia os pacotes da pasta utils
COPY src/app/utils /app/utils

EXPOSE 8501

# Comando para iniciar a aplicação
CMD ["streamlit", "run", "app.py"]