import { useState, useEffect } from 'react';
import React from 'react';
import FetchSensorReadings from './components/fetchSensorReadings';

// const sensorUrl = "http://iothydro.ddns.net/latest-readings";
const sensorUrl = "iothydro.ddns.net";

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <h2>Sensor Readings</h2>
            </header>
            <FetchSensorReadings></FetchSensorReadings>
        </div>
    )
}

export default App;