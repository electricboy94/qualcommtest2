from time import sleep

from sensor import SensorServer

if __name__ == '__main__':
    sensor_server = SensorServer()
    sensor_server.daemon = True
    sensor_server.start()

    while True:
        sensor_output = sensor_server.get_sensor_output()
        sensor_output.send

            # Sleep for 3 seconds
        sleep(3)