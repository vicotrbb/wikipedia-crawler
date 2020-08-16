# Builder
FROM python:3 AS builder
COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.8-slim

COPY . /work
WORKDIR /work

COPY --from=builder /root/.local/bin /root/.local

CMD ["python3", "crawler.py"]