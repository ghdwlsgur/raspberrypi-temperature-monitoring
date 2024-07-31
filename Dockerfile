FROM python:3.12-alpine
WORKDIR /app
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["python3", "__main__.py"]
