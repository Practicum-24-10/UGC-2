FROM python:3.10

# Выберите папку, в которой будут размещаться файлы проекта внутри контейнера
WORKDIR /storage_research

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip  \
    && pip install -r requirements.txt --no-cache-dir \
    && mkdir -p /storage_research/results

COPY . .

ENTRYPOINT ["python", "main.py"]