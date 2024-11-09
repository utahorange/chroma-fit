import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from 'react'

// function color_palette(skin, eyes, lip) {

// }

export default function App() {

  const[skin_primary_color, setSkinColor] = useState([0,0,0])
  const[average_eye_rgb, setEyeColor] = useState(0)
  const[lip_rgb, setLipColor] = useState(0)
  // const[web_content,setContent] = useState("no state")
  
  useEffect(() =>  {
    //fetch("/api/ml").then(res => res.json()).then(data => {setContent(data.face)})
    const fetchData = async () => {
      try {
        const res = await fetch("/api/ml");
        const data = await res.json();
        
        setSkinColor(data.skin_primary_color || [0, 0, 0]);
        setEyeColor(data.average_eye_rgb || 0);
        setLipColor(data.lip_rgb || 0);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();  // Call the function to fetch the data when the component mounts
  }, []);

  const skinColorStyle = {
    backgroundColor: `rgb(${skin_primary_color.join(', ')})`,
    width: '150px',
    height: '150px',
    border: '1px solid #000',
    margin: '10px auto',
  };
  
  return (
    <div className="App">
      <header className="App-header">
        <h3>Generated Palettes:</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 50px)', gridGap: '5px' }}>
          <div style={{ backgroundColor: (100,100,100), width: '50px', height: '50px' }}></div>
        </div>
        <div style={skinColorStyle}></div>
        {/* <p>
        output: {skin_primary_color}
        </p> */}
      </header>
    </div>
  );
};
