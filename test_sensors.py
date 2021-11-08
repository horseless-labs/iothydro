import time
import cv2
import RPi.GPIO as GPIO
import Adafruit_DHT

from sensor_config import *

import os
import mysql.connector as database

# Move this to a config file later
username = os.environ.get("username")
password = os.environ.get("password")

GPIO.setmode(GPIO.BOARD)

DHT_SENSOR = Adafruit_DHT.DHT11

WEBCAM_DW3_DW4 = cv2.VideoCapture(0)

for deep_water in DW:
    GPIO.setup(deep_water[0], GPIO.IN)
    GPIO.setup(deep_water[1], GPIO.OUT)

# Add code to convert these distances into volumes for each of
# the deep water bins
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

# Clarify that this the readings here are for temperature and humidity
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

def insert_readings(conn, readings):
    sql = "INSERT INTO auto_readings (date_and_time," \
        "dw3_volume," \
        "dw4_volume," \
        "temperature," \
        "humidity," \
        "dw3_and_dw4_image)"\
        "VALUE (%s, %s, %s, %s, %s, %s);"

    cursor = conn.cursor()
    cursor.execute(sql, readings)
    conn.commit()
    return cursor.lastrowid

if __name__ == '__main__':
    try:
        connection = database.connect(
            user=username,
            password=password,
            host="localhost",
            database="iothydro_db")
    except:
        print("Could not establish a connection to the database")
        exit()

    try:
        while(True):
            readings = avg_readings()
            dw3_vol = distance(DW3[0], DW3[1])
            dw4_vol = distance(DW4[0], DW4[1])

            print(readings)
            print(dw3_vol)
            print(dw4_vol)
            
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            image_fh = "DW3_DW4-" + current_time + ".jpg"

            ret, frame = WEBCAM_DW3_DW4.read()
            cv2.imwrite("images/" + image_fh, frame)

            params = []

            params.append(current_time)
            params.append(dw3_vol)
            params.append(dw4_vol)
            params.append(readings[0])
            params.append(readings[1])
            params.append(image_fh)

            insert_readings(connection, params)
            print("Insertion complete")
            print("Sleeping for 5 seconds")
            time.sleep(5)

        GPIO.cleanup()
        WEBCAM_DW3_DW4.release()
        cv2.destroyAllWindows()
    except KeyboardInterrupt:
        print("Stopped by user")

        GPIO.cleanup()
        WEBCAM_DW3_DW4.release()
        cv2.destroyAllWindows()
