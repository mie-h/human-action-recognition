FROM python:3.9

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY lambda_function_HumanActionRecognition.py .
COPY labels.txt .
COPY action_recognition.py .
COPY utils.py .
COPY main.py .

CMD ["main.py"]
ENTRYPOINT ["python"]