FROM python:3.12.2-alpine3.19

ADD . /app

WORKDIR /app

ENV PATH="/root/.cargo/bin/:$PATH"

RUN mkdir -p /app/data

RUN pip install uv

RUN uv pip install --system -r requirements.txt

EXPOSE 8000

CMD [ "/bin/bash", "start.sh" ]
