FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY datagram-loader.py ./
CMD ["python", "data-loader.py"]
