FROM a1fred/docker-python-phantomjs:py3.6-phantom2.1.1

WORKDIR /src

RUN pip install \
    influxdb \
    selenium \
    xfinity-usage

ADD send_to_influx.py .

ENV INFLUXDB_HOST=localhost INFLUXDB_PORT=8086

CMD [ "python3", "send_to_influx.py" ]
