FROM python:3.12.4

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# EXPOSE must match Cloud Run default port
EXPOSE 8080

CMD ["gunicorn", "pricing_optimization.wsgi:application", "--bind", "0.0.0.0:8080"]
