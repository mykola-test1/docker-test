FROM python:3.10

# Set the working directory
WORKDIR /app

COPY app/ .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5010

CMD ["python", "main.py"]
