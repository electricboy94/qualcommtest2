from time import sleep
while True :
    raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
    v = 5 * 0.000244140625 * raw

    t = (1000 * v) - 531

    sleep(1)

    print t