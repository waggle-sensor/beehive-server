FROM waggle/beehive-core:2

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY datagram-loader.py ./
CMD ["python", "datagram-loader.py"]
