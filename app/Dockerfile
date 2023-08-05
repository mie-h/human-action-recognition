FROM python:3.9

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY labels.txt .
COPY action_recognition.py .
COPY utils.py .
COPY main.py .

# how to start from main function?
CMD ["main.py"]
ENTRYPOINT ["python"]