import logging
import sqlite3
from neo import Gpio
from threading import Thread
from threading import Lock
from time import sleep, time

logger = logging.getLogger(__name__)


class SensorServer(Thread):
    """Sensor server that keeps reading sensors and provide get_sensor_output() method for user"""

    def __init__(self):                       # consturcter 이다, 초기화
        # Parent class constructor
        Thread.__init__(self)

        # Assign GPIO pins that controls MUX, LSB to MSB
        self.gpio_pins = [24, 25, 26, 27]     # 먹스에 저거네개를 끼운다 (사진)
        self.gpio = Gpio()              # 새 Gpio 라이브러리
        # Set GPIO pins to output
        try:
            for pin in self.gpio_pins:
                self.gpio.pinMode(pin, self.gpio.OUTPUT)   # 24 245 26 27 아웃풋
        except Exception as e:
            logger.error("Error setting GPIO pin, reason %s" % e.message)
            print "Error setting GPIO pin %d, reason %s" % e.message

        # Use A0 port
        self.adc_raw = "/sys/bus/iio/devices/iio:device0/in_voltage0_raw"    #ADC로 읽은 파일 연다
        self.adc_scale = "/sys/bus/iio/devices/iio:device0/in_voltage_scale"

        self.sensor_names = ['Temp', 'SN1', 'SN2', 'SN3', 'SN4', 'PM25']     # 센서네임

        # Use a dict to store sensor output, the format is:
        # { "time": [time stamp],
        #   [sensor1 name]: [sensor1 output],
        #   ...
        #   [sensor6 name]: [sensor6 output]}
        self.sensor_output = {}         #아웃풋에 대한 새로운 오브젝트만들고

        # Create a lock to protect sensor output. That is, when updating the result, lock it on to prevent it from being
        # read at the same time; similarly, when reading the result, lock it on to prevent it from being updated.
        self.sensor_output_lock = Lock()     # 멀티플 트레드 가질때  막는다... ? 한번에 많은 쓰레드가 ? 컨넥하는것ㅇ르 막는다 . 이상한값 안나오게하려고 하는듯

        self.db_conn = sqlite3.connect("air_pollution_data.db")
        self.db_cur = self.db_conn.cursor()
        for sensor_name in self.sensor_names:
            self.db_cur.execute("CREATE TABLE IF NOT EXISTS %s (time int PRIMARY KEY NOT NULL, value real)" % sensor_name)

    def get_sensor_output(self):
        # Get the latest sensor output
        return self.sensor_output.copy()

    def set_mux_channel(self, m):                    #먹스체널 정한다. example 15 =1111 .
        # Set MUX channel
        # Convert n into a binary string
        bin_repr = "{0:04b}".format(m)
        # Assign value to pin
        for i in xrange(0, 4):
            self.gpio.digitalWrite(24 + i, bin_repr[i])

    def read_sensor(self, n):
        # Read raw data from sensor n, we allocate 2 channels for each sensor:
        # sensor 0: channel 0, 1
        # sensor 1: channel 2, 3
        # ...
        # sensor 7: channel 15, 16

        # Set MUX to read the first channel
        try:
            self.set_mux_channel(2 * n)
            v1 = int(open(self.adc_raw).read()) * float(open(self.adc_scale).read())

            # Set MUX to read the second channel
            self.set_mux_channel(2 * n + 1)
            v2 = int(open(self.adc_raw).read()) * float(open(self.adc_scale).read())

            return v1, v2
        except Exception as e:
            logger.error("Error reading sensor %d, reason: %s" % (n, e.message))
            print "Error reading sensor %d, reason: %s" % (n, e.message)
            return 0.0, 0.0

    def run(self):                          # 루프 계속 진행
        # Keep reading sensors
        while True:
            # Acquire the lock
            self.sensor_output_lock.acquire()
            # Add time stamp
            self.sensor_output['time'] = int(time())

            # Do sensor reading here
            #  1. set MUX to sensor 1, read sensor 1;
            #  2. set MUX to sensor 2, read sensor 2;
            #  ...
            #  n. set MUX to sensor n, read sensor n.
            for i in xrange(0, 6):
                logger.info("Reading %s sensor..." % self.sensor_names[i])
                print "Reading %s sensor..." % self.sensor_names[i]
                v1, v2 = self.read_sensor(i)       #   63 번에 n이 여기서 i 야
                self.sensor_output[self.sensor_names[i]] = v1 - v2

            self.sensor_output_lock.release()

            # Idle for 3 seconds
            sleep(3)
