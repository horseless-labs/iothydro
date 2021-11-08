# sleep_duration is the time between readings
sleep_duration = 600.0

# readings_relay is a sensor calibration time
readings_delay = 2.0

# The number of time the DHT11 temperature and humidity sensor
# takes readings, which are then averaged into one final number.
readings_num = 10.0

# ECHO and TRIG pins for the HC-SR04 sensors
DW3 = [38, 40]
DW4 = [35, 37]
DW = [DW3, DW4]

# Data pin for the DHT11 sensor
DHT_PIN = 4