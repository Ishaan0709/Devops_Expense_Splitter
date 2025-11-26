# 1. Base image - Python ka chhota slim version
FROM python:3.11-slim

# 2. Container ke andar working directory
WORKDIR /app

# 3. Dependencies file copy karo
COPY requirements.txt .

# 4. Dependencies install karo
RUN pip install --no-cache-dir -r requirements.txt

# 5. Baaki saara code copy karo
COPY . .

# 6. Flask app jo port use karega
EXPOSE 5000

# 7. Container start hone par yeh command chalegi
CMD ["python", "app.py"]
