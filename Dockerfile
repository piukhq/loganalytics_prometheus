FROM ghcr.io/binkhq/python:3.10 AS build

WORKDIR /src

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY . .

RUN poetry build

FROM ghcr.io/binkhq/python:3.10

ARG wheel=loganalytics_prometheus-*-py3-none-any.whl

WORKDIR /app
COPY --from=build /src/dist/$wheel .
RUN pip install $wheel && rm $wheel

CMD ["/usr/local/bin/loganalytics_prometheus"]
