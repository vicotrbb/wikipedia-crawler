FROM python:3.8-slim

COPY . /work
WORKDIR /work

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "crawler.py"]