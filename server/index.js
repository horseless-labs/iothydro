const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const mysql = require('mysql')
const { restart } = require('nodemon')
const latestReadings = require('./routes/latestReadingsRouter')

const path = require('path')
const envPath = path.resolve(process.cwd(), '.env.local')

require('dotenv').config({ path: envPath })

// const db = mysql.createPool({
//     host: process.env.MYSQL_HOST,
// 	user: process.env.MYSQL_USERNAME,
// 	password: process.env.MYSQL_PASSWORD,
// 	port: process.env.MYSQL_PORT,
// 	database: process.env.MYSQL_DATABASE,
// })

// app.get('/', (req, res) => {
//     let timestamp = ''
//     let temp = ''
//     let hum = ''
//     let distance = ''
//     let outputs = ''

//     let sql = "SELECT * FROM readings ORDER BY id DESC LIMIT 0,1";
//     db.query(sql, (err, result) => {
//         if (err) throw err

// 		outputs = result
// 		timestamp = result[0].timestamp
// 		temp = result[0].temperature
// 		hum = result[0].humidity
// 		distance = result[0].distance

// 		res.send(outputs)
//     })
// })

app.use(bodyParser.json())
app.use(
    bodyParser.urlencoded({
        extended: true,
    })
)

app.get('/', (req, res) => {
    res.json({'status': 'ok'})
})

app.use('/latest-readings', latestReadings);

app.use((err, req, res, next) => {
    const statusCode = err.statusCode || 500;
    console.error(err.message, err.stack);
    res.status(statusCode).json({'message': err.message})

    return;
})

app.listen(3001, () => {
    console.log('running on port 3001')
})