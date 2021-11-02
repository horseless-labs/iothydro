const db = require('./db');
const config = require('../config');

async function getLatest() {
    // Currently limited to just the latest readings
    const row = await db.query(`SELECT * FROM readings ORDER BY id DESC LIMIT 0, 1`);

    return row[0];
}

module.exports = {
    getLatest
}