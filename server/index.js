const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const mysql = require('mysql')
const { restart } = require('nodemon')
const latestReadings = require('./routes/latestReadingsRouter')

const path = require('path')
const envPath = path.resolve(process.cwd(), '.env.local')

require('dotenv').config({ path: envPath })

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