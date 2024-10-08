FROM python:3.12.5

# Instalar FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

COPY ./app /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]