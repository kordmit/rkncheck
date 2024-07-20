FROM python:latest
ENV dir=/app
WORKDIR $dir
COPY . $dir
RUN apt-get update && apt-get install python3 && pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]
