from btserver import BTServer
from bterror import BTError

import argparse
import asyncore
import json
from random import uniform
from threading import Thread
from time import sleep, time

if __name__ == '__main__':
    # Create option parser
    usage = "usage: %prog [options] arg"
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", dest="output_format", default="csv", help="set output format: csv, json")

    args = parser.parse_args()

    # Create a BT server
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_name = "GossipBTServer"
    server = BTServer(uuid, service_name)

    # Create the server thread and run it
    server_thread = Thread(target=asyncore.loop, name="Gossip BT Server Thread")
    server_thread.daemon = True
    server_thread.start()

    while True:
        msg = ""
        sensor_output = sensor_server.get_sensor_output()
        epoch_time = int(time())                    # epoch time
        temp = sensor_output.get('Temp', -1)
        SN1 = sensor_output.get('SN1', -1)
        SN2 = sensor_output.get('SN2', -1)
        SN3 = sensor_output.get('SN3', -1)
        SN4 = sensor_output.get('SN4', -1)
        PM25 = sensor_output.get('PM25', -1)

            msg = ""
            if args.output_format == "csv":
                msg = "realtime, %d, %f, %f, %f, %f, %f, %f" % (epoch_time, round(temp,2), round(SN1,2), round(SN2,2), round(SN3,2), round(SN4,2), round(PM25,2))
            elif args.output_format == "json":
                output = {'type': 'realtime',
                          'time': epoch_time,
                          'TEMP': round(temp,2),
                          'CO': round(SN1,2),
                          'NO2': round(SN2,2),
                          'SO2': round(SN3,2),
                          'O3': round(SN4,2),
                          'PM25': round(PM25,2),
                          }
                msg = json.dumps(output)
            try:
                client_handler.send(msg + '\n')
            except Exception as e:
                BTError.print_error(handler=client_handler, error=BTError.ERR_WRITE, error_message=repr(e))
                client_handler.handle_close()

            # Sleep for 3 seconds
        sleep(3)
