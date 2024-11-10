import React, { useState } from 'react'

export default function Input(props) {

  const[current,setCurrent]=useState()
  return (
    <div style={{width:"80%"}}>
        <br></br><br></br>
      <div className="input-group" >

  <span class="input-group-text">Enter details of the movie</span>
  <textarea class="form-control" aria-label="With textarea" onChange={(e) => setCurrent(e.target.value)}></textarea>
  
</div>
<br></br>
<button type="button" class="btn btn-primary"  style={{width:"40%"}}  onClick={() => {
        console.log("Button clicked")
        props.setText(current)
        props.setLoading(true)
      }}>Click here to search for the movie..</button>
    </div>
  )
}
