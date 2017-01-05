FROM python:3.6

RUN mkdir /code
ADD requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

ADD . /code

CMD ["python", "main.py"]