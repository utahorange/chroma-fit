import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from 'react'

function App() {

  const[skin_primary_color, setAccuracy] = useState(0)

  useEffect(() =>  {

  },[])
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
        Output: {skin_primary_color}
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
