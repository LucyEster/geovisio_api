# Use a imagem oficial do Python como imagem base
FROM python:3.12

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do código fonte para o diretório de trabalho
COPY . .

# Define o comando padrão a ser executado quando o container for iniciado
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]