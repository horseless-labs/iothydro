import { useState, useEffect } from 'react';
import React from 'react';
import FetchSensorReadings from './components/fetchSensorReadings';

const sensorUrl = "http://iothydro.ddns.net/latest-readings";

function App() {
    const [userData, setUserData] = useState({});

    // useEffect(() => {
    //     getSensorDataWithFetch();
    // }, []);

    // const getSensorDataWithFetch = async () => {
    //     const response = await fetch(sensorUrl, {mode: 'cors'});
    //     const jsonData = await response.text();
    //     setUserData(jsonData);
    //     console.log(userData)
    // };

    return (
        <div className="App">
            <header className="App-header">
                <h2>Sensor Readings</h2>
            </header>
            {/* <div className="user-container">
                <h5 className="timestamp">{userData}</h5>
            </div> */}
            <FetchSensorReadings></FetchSensorReadings>
        </div>
    )
}

export default App;