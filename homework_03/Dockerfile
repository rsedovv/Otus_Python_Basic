# Используем базовый образ Python
FROM python:3.10-slim-buster

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем требования
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект внутрь образа
COPY . .

# Открываем порт 8000
EXPOSE 8000

# Запускаем сервер uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Примечание: Контейнер можно запустить следующей командой:
# docker run -p 8000:8000 my_app_image