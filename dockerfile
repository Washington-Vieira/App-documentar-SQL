# Use a imagem base oficial do Python
FROM python:3.12-slim

# Instalar Git e outras ferramentas necessárias
RUN apt-get update && apt-get install -y git && apt-get clean

# Defina o diretório de trabalho dentro do container
WORKDIR /doc sql

# Clonar o repositório Git (substitua pelo URL do seu repositório)
RUN git clone https://github.com/Washington-Vieira/App-documentar-SQL.git .

#Definine a pasta do repositório como diretório de trabalho
WORKDIR /doc sql

# Copie apenas o arquivo requirements.txt primeiro (para otimizar o cache do Docker)
COPY minha_documentacao/requirements.txt ./minha_documentacao/requirements.txt

# Instale as dependências a partir do requirements.txt
WORKDIR /doc sql/minha_documentacao
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copie o restante do projeto para o container
WORKDIR /doc sql
COPY . .

# Alterar para o diretório 'minha_documentacao' antes de executar o app
WORKDIR /doc sql/minha_documentacao

# Exponha a porta usada pelo Streamlit
EXPOSE 58888
#8501

# Comando para rodar a aplicação Streamlit
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "58888"]