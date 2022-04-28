FROM python:alpine3.15

COPY . /grant-tracking-backend
WORKDIR /grant-tracking-backend

RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/grant-tracking-backend"

EXPOSE 8085
ENTRYPOINT [ "python3" ]