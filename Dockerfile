FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip3 install -r requirements.txt

COPY lambda_functionHumanActionRecognition.py ${LAMBDA_TASK_ROOT}
COPY labels.txt ${LAMBDA_TASK_ROOT}
COPY action_recognition.py ${LAMBDA_TASK_ROOT}
COPY utils.py ${LAMBDA_TASK_ROOT}


CMD [ "lambda_functionHumanActionRecognition.lambda_handler" ]