import Adafruit_DHT
import RPi.GPIO as GPIO
import time, datetime

import os
import mysql.connector as database

username = os.environ.get("username")
password = os.environ.get("password")

connection = database.connect(
        user=username,
        password=password,
        host="localhost",
        database="sensors")

# Preliminary configurations that deal with one of each sensor
# This is subject to expansion in the future.
readings_delay = 2.0
readings_num = 2.0

# Setup for DHT11 humidity and temperature sensor
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

# Setup for HR-SR04 ultrasonic rangefinder
GPIO.setmode(GPIO.BOARD)
TRIG = 16
ECHO = 18

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def distance():
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
        # Return these in the event of sensor failure
        # Think of something else
        return [0, 0]

# Take readings_num readings and average the results
def avg_readings():
    hums = []
    temps = []
    dists = []

    # Observed sensor/wiring failure sometimes makes the
    # number of readings here less than readings_num
    # Rough: currently does not take into account the chance
    # of a total sensor failure, just the one-offs that have
    # been observed so far.
    th_count = 0
    for i in range(int(readings_num)):
        print("Taking reading #" + str(i))
        temp, hum = temp_and_hum()
        if temp != 0:
            th_count += 1
            temps.append(temp)
        if hum != 0:
            hums.append(hum)

        dists.append(distance())
        time.sleep(readings_delay)

    hum_avg = sum(hums)/th_count
    temp_avg = sum(temps)/th_count
    dist_avg = sum(dists)/readings_num
    timestamp = str(datetime.datetime.today().replace(microsecond=0))

    # Preliminary data to be loaded into a test database
    return [timestamp, temp_avg, hum_avg, dist_avg]

def insert_readings(conn, readings):
    sql = "INSERT INTO readings (timestamp, temperature, humidity, distance) VALUE (%s, %s, %s, %s);"
    cursor = conn.cursor()
    cursor.execute(sql, readings)
    conn.commit()
    return cursor.lastrowid

if __name__ == '__main__':
    connection = database.connect(
            user=username,
            password=password,
            host="localhost",
            database="sensors")

    try:
        while True:
            readings = avg_readings()
            insert_readings(connection, readings)
            print(readings)

            time.sleep(readings_delay)
    except KeyboardInterrupt:
        print("Stopped by user")
        GPIO.cleanup()
        connection.close()
