FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY log-saver.py ./
CMD ["python", "./log-saver.py"]
