
FROM python:3.10-slim

# 2. Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# 3. Copie o arquivo de requisitos
COPY requirements.txt .

# 4. Instale TODAS as bibliotecas (incluindo psycopg2)
# O --no-cache-dir mantém a imagem um pouco menor
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copie o resto do seu código (ex: app.py)
COPY . .

CMD ["flask", "main.py"]
# O comando para rodar a aplicação será dado pelo docker-compose.yml