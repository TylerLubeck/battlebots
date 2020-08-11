FROM python:3.8

WORKDIR /app
COPY . /app
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python", "-m", "battlebot"]
