FROM python:3

WORKDIR /usr/src/app

# install python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy local scripts
COPY . .

CMD ["python", "./worker.py"]
