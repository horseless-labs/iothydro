import React from 'react';
import { useState, useEffect } from 'react';

const FetchSensorReadings = ({}) => {
    const [state, setState] = useState({loading: true, stateData: {}});

    async function componentMounted() {
        const url = "http://iothydro.ddns.net/latest-readings";
        const response = await fetch(url, {mode: 'cors'});
        console.log(response);
        const data = await response.json();
        setState({loading: false, stateData: data})
        console.log(state);
    }

    //componentMounted();
    useEffect(() => {
        componentMounted();
    }, [])

    return (

        <div>
            {state.loading ? <div>Loading...</div> : <div>Timestamp: <div>{state.stateData.timestamp}</div></div>}
        </div>
    );
}

export default FetchSensorReadings;