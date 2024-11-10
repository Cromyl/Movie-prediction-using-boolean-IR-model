import logo from './logo.svg';
import './App.css';
import Navbar from './components/Navbar';
import Input from './components/Input';
import { useState } from 'react';
// import MovieCard from './components/MovieCard';
import Result from './components/Result';

function App() {

  const [text,setText] = useState('')
  const [loading, setLoading] = useState(true); 

  return (
    <>
    <Navbar/>
    <div className="App" style={{ display: "flex", justifyContent: "center", width: "100%", flexDirection: "column", alignItems: "center" }}>

      
      
      <Input setText={setText} setLoading={setLoading}/>
      <br></br><br></br>
      <Result text={text} loading={loading} setLoading={setLoading}/>
      {/* <MovieCard/>
      <MovieCard/>
      <MovieCard/> */}
    </div>
    </>
  );
}

export default App;
