FROM python:3.9 as base

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir -r requirements/prod.txt

FROM base AS tests
RUN pip install --no-cache-dir -r requirements/dev.txt
RUN make pylint && \
    make black

FROM base AS build
CMD ["make", "app"]