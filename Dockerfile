FROM python:3.13.3-alpine
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["uvicorn", "routers:app", "--host", "0.0.0.0", "--port", "5000"]