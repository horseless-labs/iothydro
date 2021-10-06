const express = require('express');
const router = express.Router();
const latestReadings = require('../services/latestReadings');

router.get('/', async function(req, res, next) {
    try {
        res.json(await latestReadings.getLatest());
    } catch (err) {
        console.error(`Error while getting readings from the database `, err.message);
        next(err);
    }
});

module.exports = router;