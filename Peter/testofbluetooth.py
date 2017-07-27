from time import sleep

from sensor import SensorServer

if __name__ == '__main__':
    sensor_server = SensorServer()
    sensor_server.daemon = True
    sensor_server.start()

    while True:
        sensor_output = sensor_server.get_sensor_output()

            try:
                sensor_output.send(msg)
            except Exception as e:
                BTError.print_error(handler=client_handler, error=BTError.ERR_WRITE, error_message=repr(e))
                client_handler.handle_close()

            # Sleep for 3 seconds
        sleep(3)