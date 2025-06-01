FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENV FLASK_ENV=production
COPY . /app 
CMD ["python", "app.py"]
