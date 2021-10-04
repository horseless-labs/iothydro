import React, { useState, useEffect } from 'react'
import Axios from 'axios'
import './App.css'
const bodyParser = require('body-parser')

function App() {
  const [temperature, setTemperature] = useState('')
  const [humidity, setHumidity] = useState('')
  const [distance, setDistance] = useState('')
  const [timestamp, setTimestamp] = useState('')

  useEffect(() => {
    Axios.get('iothydro.ddns.net/api/get').then((response) => {
      console.log(response)
    })
  })

  return (
    <div className="App">
      <h1>Hydroponics IoT</h1>

      <div className="form">
        <label>Timestamp</label>

      </div>
    </div>
  );
}

export default App;
