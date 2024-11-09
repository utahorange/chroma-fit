import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from 'react'

function App() {

  const[skin_primary_color, setSkinColor] = useState(0)
  const[average_eye_rgb, setEyeColor] = useState(0)
  const[lip_rgb, setLipColor] = useState(0)
  const[web_content,setContent] = useState("no state")
  
  useEffect(() =>  {
    //fetch("/api/ml").then(res => res.json()).then(data => {setSkinColor(data.skin_primary_color);setEyeColor(data.average_eye_rgb);setLipColor(data.lip_rgb)})
    fetch("/api/ml").then(res => res.json()).then(data => {setContent(data[0][0])})
  },[])
  
  return (
    <div className="App">
      <header className="App-header">
        <h3>Generated Palettes:</h3>
        <p>
        output: {web_content}
        </p>
      </header>
    </div>
  );
}

export default App;
