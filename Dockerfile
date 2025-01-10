FROM python:latest
RUN apt update -y && \
    apt upgrade -y && \
    apt install -y --no-install-recommends \
    python3-pip && \
    apt autoremove -y && \
    rm -rf /var/lib/apt/lists/*
# Копирование файлов в рабочую директорию
COPY . /TestFlaskTask
# Установка рабочей директории
WORKDIR /TestFlaskTask
# Установка зависимостей
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements/requirements.txt
# Запуск приложения
ENV HOST=0.0.0.0
ENV PORT=8000
EXPOSE ${PORT}
CMD ["python3", "-m", "src.app"]