const { readFileSync, writeFileSync } = require('fs');
const sqlite3 = require('sqlite3').verbose()

const express = require('express');
const app = express();

let path = "/home/pi/iothydro"

let db = new sqlite3.Database(path + "/sensor_readings.db")
let sql = "SELECT * FROM readings ORDER BY id DESC LIMIT 0,1";
let timestamp = ''
let temp = ''
let hum = ''
let distance = ''
let result = db.get(sql, (err, row) => {
	timestamp = row.timestamp
	temp = row.temperature
	hum = row.humidity
	distance = row.distance
})

app.get('/', (req, res) => {
	res.send(`
		<!DOCTYPE html>
		<html lang='en'>
		<head>
			<meta http-equiv="refresh" content="60" />
			<meta charset='utf-8' />
			<meta name='viewport' content='width=device-width, initial-scale=1' />
		</head>
		<body>
		<h1>Most Recent Sensor Readings</h1>
		<p>${timestamp}, ${temp}, ${hum}, ${distance}</p>
		</body>
		</html>`)
});

app.listen(5000, () => console.log('http:localhost:5000'));
