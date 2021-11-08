"""
##### ATTENTION #####
This script is meant to run on a Raspberry Pi 4. As you can see below,
it imports several libraries to that effect. It isn't plug-and-play with a
given computer.
"""

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

# Setting this up for future expansion: the current plan has it that there
# will be 4-5 deep water systems in need of monitoring shortly.
for deep_water in DW:
    GPIO.setup(deep_water[0], GPIO.IN)
    GPIO.setup(deep_water[1], GPIO.OUT)

# TODO: Add code to convert these distances into volumes for each of
# the deep water bins
def distance(ECHO, TRIG):
    # Power cycle the pin for calibration purposes
    GPIO.output(TRIG, False)
    time.sleep(readings_delay)

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

# Get a single reading from the DHT11 sensor
def temp_and_hum():
    hum, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if hum is not None and temp is not None:
        return [temp, hum]
    else:
        # Might reconsider this.
        return [0, 0]

# Get a number of temperature and humidity readings that is specified in
# the sensor_config.py file.
# Multiple readings are needed because the sensor has occasional one-off
# failures that need to be rounded out.
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

# Insert readings into MySQL database, currently iothydro_db
# TODO: try except statement here.
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
    # Attempt connection to the database.
    try:
        connection = database.connect(
            user=username,
            password=password,
            host="localhost",
            database="iothydro_db")
    except:
        print("Could not establish a connection to the database")
        exit()

    # Try to take readings and insert them into the database.
    try:
        # TODO: replace this loop with a schedule and a pause mechanism
        # TODO: move the camera to a schedule, and possibly use the most
        #       recent as a placeholder in the database. They will only
        #       be black when the lights are out.
        while(True):
            # readings here is temp and humidity
            readings = avg_readings()

            dw3_vol = distance(DW3[0], DW3[1])
            dw4_vol = distance(DW4[0], DW4[1])

            """
            print(readings)
            print(dw3_vol)
            print(dw4_vol)
            """

            # Time format needed for compatibility with MySQL DATETIME
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')

            # Filename of the image
            # Images themselves are not stored in the database.
            # They can be found in the images/ directory
            image_fh = "DW3_DW4-" + current_time + ".jpg"

            # Capture a single frame and write it to images/
            ret, frame = WEBCAM_DW3_DW4.read()
            cv2.imwrite("images/" + image_fh, frame)

            # Easiest way to do this given the way MySQL needs the params
            # to be inserted. It's not a big deal; don't touch it.
            params = []

            params.append(current_time)
            params.append(dw3_vol)
            params.append(dw4_vol)
            params.append(readings[0])
            params.append(readings[1])
            params.append(image_fh)

            insert_readings(connection, params)
            print("Insertion complete")

            # Wait 10 minutes before taking more readings.
            # This level of granularity might be unnecessary for our purposes.
            print(f"Sleeping for {sleep_duration} seconds.")
            time.sleep(sleep_duration)

        GPIO.cleanup()
        WEBCAM_DW3_DW4.release()
        cv2.destroyAllWindows()
    except KeyboardInterrupt:
        print("Stopped by user")

        GPIO.cleanup()
        WEBCAM_DW3_DW4.release()
        cv2.destroyAllWindows()
