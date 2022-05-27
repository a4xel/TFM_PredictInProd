FROM python:3.8.12

COPY TaxiFareModel  /TaxiFareModel
COPY requirements.txt /requirements.txt
COPY api /api
COPY my_new_model /my_new_model

RUN pip3 install --upgrade pip
RUN pip3 install Cython
RUN pip3 install -r requirements.txt


CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT








