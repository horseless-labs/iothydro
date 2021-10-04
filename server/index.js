const express = require('express')
const app = express()
const mysql = require('mysql')
const { restart } = require('nodemon')

const path = require('path')
const envPath = path.resolve(process.cwd(), '.env.local')

require('dotenv').config({ path: envPath })

const db = mysql.createPool({
    host: process.env.MYSQL_HOST,
	user: process.env.MYSQL_USERNAME,
	password: process.env.MYSQL_PASSWORD,
	port: process.env.MYSQL_PORT,
	database: process.env.MYSQL_DATABASE,
})

app.get('/', (req, res) => {
    let timestamp = ''
    let temp = ''
    let hum = ''
    let distance = ''
    let outputs = ''

    let sql = "SELECT * FROM readings ORDER BY id DESC LIMIT 0,1";
    db.query(sql, (err, result) => {
        if (err) throw err

		outputs = result
		timestamp = result[0].timestamp
		temp = result[0].temperature
		hum = result[0].humidity
		distance = result[0].distance

		res.send(outputs)
    })
})

app.listen(3001, () => {
    console.log('running on port 3001')
})