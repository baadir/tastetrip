FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DATA_DIR=/app/data PORT=8080 COOKIE_SECURE=true
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd --create-home --uid 10001 tastetrip && mkdir /app/data && chown tastetrip:tastetrip /app/data
COPY app ./app
USER tastetrip
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 CMD python -c "import os,urllib.request; urllib.request.urlopen('http://127.0.0.1:'+os.getenv('PORT','8080')+'/health',timeout=3)"
CMD ["sh", "-c", "exec gunicorn 'app.server:create_app()' --bind 0.0.0.0:${PORT:-8080} --workers 1 --threads 8 --timeout 180 --graceful-timeout 30 --access-logfile - --error-logfile -"]
