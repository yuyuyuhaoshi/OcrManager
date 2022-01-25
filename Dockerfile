FROM python:3.9-slim

COPY . /root/ocr-manager

WORKDIR /root/ocr-manager

RUN pip3 install -r requirements.txt

CMD ["python3", "-m", "manager.main"]
