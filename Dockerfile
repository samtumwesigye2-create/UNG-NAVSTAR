FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app app
RUN mkdir -p data
ENV PORT=8000
CMD ["sh","-c","uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]

HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"
