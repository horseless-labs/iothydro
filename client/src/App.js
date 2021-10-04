import './App.css';
import React, { useState, useEffect } from 'react';

function App() {
  const [temperature, setTemperature] = useState('')
  const [humidity, setHumidity] = useState('')
  const [distance, setDistance] = useState('')
  const [timestamp, setTimestamp] = useState('')

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
