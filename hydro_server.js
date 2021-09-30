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

let sql = "SELECT * FROM readings ORDER BY id DESC LIMIT 0,1";
let timestamp = ''
let temp = ''
let hum = ''
let distance = ''
let outputs = ''
db.connect(function(err) {
	if (err) throw err;

	db.query(sql, function(err, result) {
		if (err) throw err
		outputs = result
		timestamp = result[0].timestamp
		temp = result[0].temperature
		hum = result[0].humidity
		distance = result[0].distance
	})
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
