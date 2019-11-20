import os
import sys
import time
from datetime import datetime
from influxdb import InfluxDBClient
from xfinity_usage.xfinity_usage import XfinityUsage

def main():
    xfinity_username = os.environ.get('XFINITY_USERNAME')
    xfinity_password = os.environ.get('XFINITY_PASSWORD')

    if not (xfinity_username and xfinity_password):
        print("Missing xfinity username and password")
        sys.exit(1)

    xfinity = XfinityUsage(
        username=xfinity_username,
        password=xfinity_password,
        debug=False
    )

    influx_host = os.environ.get('INFLUXDB_HOST')
    influx_port = int(os.environ.get('INFLUXDB_PORT')) if os.environ.get('INFLUXDB_PORT') else None
    influx_db = os.environ.get('INFLUXDB_DB')

    delay = int(os.environ.get('DELAY')) if os.environ.get('DELAY') else 3600

    influx_client = InfluxDBClient(influx_host, influx_port, database=influx_db)

    while True:
        try:
            print("Getting Comcast usage data")
            res = xfinity.run()

            timestamp = datetime.fromtimestamp(res['data_timestamp'])

            points = [{
                'measurement': 'xfinity_usage',
                'time': timestamp.isoformat(),
                'fields': {
                    'used': res['used'],
                    'total': res['total'],
                }
            }]

            print("Writing usage data to influxdb")
            influx_client.write_points(points)
        except Exception as e:
            import traceback
            traceback.print_exc()

        print("Sleeping %s seconds" % delay)
        time.sleep(delay)


if __name__ == "__main__":
    main()
