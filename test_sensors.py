import time
import cv2
import RPi.GPIO as GPIO
import Adafruit_DHT

from sensor_config import *

GPIO.setmode(GPIO.BOARD)

DHT_SENSOR = Adafruit_DHT.DHT11

WEBCAM_DW3_DW4 = cv2.VideoCapture(0)

for deep_water in DW:
    GPIO.setup(deep_water[0], GPIO.IN)
    GPIO.setup(deep_water[1], GPIO.OUT)

def distance(ECHO, TRIG):
    GPIO.output(TRIG, False)
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    duration = stop_time - start_time
    distance = duration * 17150

    return round(distance, 1)

def temp_and_hum():
    hum, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if hum is not None and temp is not None:
        return [temp, hum]
    else:
        return [0, 0]

def avg_readings():
    hums = []
    temps = []
    th_count = 0

    for i in range(int(readings_num)):
        temp, hum = temp_and_hum()

        if temp != 0:
            th_count += 1
            temps.append(temp)
        if hum != 0:
            hums.append(hum)

    # Considering changing this such that a th_count of 0, meaning that
    # no data was recorded, returns either a null value or some interpolated
    # value
    hum_avg = sum(hums)/th_count
    temp_avg = sum(temps)/th_count
    return [temp_avg, hum_avg]

if __name__ == '__main__':
    try:
        while(True):
            print(avg_readings())
            print(distance(DW3[0], DW3[1]))
            print(distance(DW4[0], DW4[1]))
            ret, frame = WEBCAM_DW3_DW4.read()
            cv2.imwrite("DW3_DW4-" + time.asctime() + ".jpg", frame)
            time.sleep(600)

        GPIO.cleanup()
        WEBCAM_DW3_DW4.release()
        cv2.destroyAllWindows()
    except KeyboardInterrupt:
        print("Stopped by user")

        GPIO.cleanup()
        WEBCAM_DW3_DW4.release()
        cv2.destroyAllWindows()
