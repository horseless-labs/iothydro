import React from 'react';
import { useState } from 'react';

const FetchSensorReadings = ({}) => {
    const [state, setState] = useState({loading: true, stateData: []});

    async function componentMounted() {
        const url = "iothydro.ddns.net/latest-readings";
        const response = await fetch(url);
        const data = await response.json();
        setState({loading: false, stateData: data})
        console.log(state);
    }

    return (
        <div>
            {state.loading ? <div>Loading...</div> : <div>Timestamp: {state.stateData.timestamp}</div>}
        </div>
    );
}

export default FetchSensorReadings;