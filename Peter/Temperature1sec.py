from time import sleep
while True :
    raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
    print raw
    sleep(1)
    