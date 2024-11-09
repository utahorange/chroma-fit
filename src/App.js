import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from 'react'

function App() {

  const[skin_primary_color, setColors] = useState(0)

  useEffect(() =>  {
    fetch("/api/ml").then(res => res.json()).then(data => {setColors(data.skin_primary_color)})
  },[])
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
        Output: {skin_primary_color}
        </p>
      </header>
    </div>
  );
}

export default App;
