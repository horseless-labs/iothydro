const { readFileSync, writeFileSync } = require('fs')
const mysql = require('mysql')

const express = require('express')
const app = express()

const path = require('path')
const envPath = path.resolve(process.cwd(), '.env.local')

require('dotenv').config({ path: envPath })

let db = mysql.createConnection({
	host: process.env.MYSQL_HOST,
	user: process.env.MYSQL_USERNAME,
	password: process.env.MYSQL_PASSWORD,
	port: process.env.MYSQL_PORT,
	database: process.env.MYSQL_DATABASE,
});

let sql = "SELECT * FROM auto_readings ORDER BY id DESC LIMIT 0,1";
let timestamp = ''
let temp = ''
let hum = ''
let distance1 = ''
let distance2 = ''
let outputs = ''
//let img_path = "ueg.jpg"
let img_path = "hell-fire.jpg"

db.connect(function(err) {
	if (err) throw err;

	db.query(sql, function(err, result) {
		if (err) throw err
		outputs = result
		timestamp = result[0].date_and_time
		temp = result[0].temperature
		hum = result[0].humidity
		distance1 = result[0].dw3_volume
		distance2 = result[0].dw4_volume
		//img_path += result[0].dw3_and_dw4_image
		console.log(img_path)
	})
})

app.use(express.static('images'))

// HTML displahy of the latest readings
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
		<p>${timestamp}, ${temp}, ${hum}, ${distance1}, ${distance2}</p>
		<img src="${img_path}" alt="Cannot load image">
		</body>
		</html>`)
});

// JSON representation of latest database readings
// Here to be accessed from offsite
app.get('/raw', (req, res) => {
	res.json(
		{'timestamp': timestamp, 'temperature': temp, 'humidity': hum, 'distance1': distance1, 'distance2': distance2, 'img_path': img_path}
	)
})

// HTML access of a single image
app.get('/image', (req, res) => {
	res.sendFile(__dirname + "/index.html");
})

app.listen(5000, () => console.log('http:localhost:5000'));
