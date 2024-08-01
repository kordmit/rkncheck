FROM python:latest
LABEL LABEL maintainer="kordmit"
WORKDIR /app
COPY . .
RUN apt-get update && pip install --upgrade pip && pip install -r requirements.txt
CMD ["python", "bot.py"]
