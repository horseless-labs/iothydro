## IoTHydro
IoTHydro is a simple IoT monitoring system for a hydroponics project. It uses a Raspberry Pi 4 to gather data from cameras and sensors, write that data to a MySQL database, and serve it to the Internet

## Current Sensors  
- HC-SR04 ultrasonic rangefinders (x2)
- DHT-11 temperature and humidity sensor (x1)
- Webcam (x1)

## A note about the file structure
Active development is currently being done on a desktop computer, and changes are made to the Pi remotely. Being that the project is still in very early development, the file structure has evolved in a way that might be considered a bit strange. Sensor data is currently gathered from test_sensors.py, and node is used to serve the page created in hydro_server.js. As the project matures, these will be moved into the server/ directory.

Additionally, you might notice that there is relatively little development in the client/ directory. Due to historial accident, the files that will one day live there are located in the server/ directory. Apologies for the confusion.