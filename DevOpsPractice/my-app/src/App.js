import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [counter, setCounter ] = useState({'counter': 0});

  const fetchCounterData = () => {
    fetch(`${process.env.REACT_APP_BACKEND_URL}/counter`)
      .then(res => {
        return res.json();
      })
      .then(data => {
        setCounter(data);
      })
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
