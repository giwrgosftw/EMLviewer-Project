// Main.jsx - 2nd front-end entry component, is connected with App.jsx
// What the user sees/interacts, as here, the front-end connects with the back-end

import React from 'react';
import { Button, Grid, Row, Col } from "react-bootstrap";
// var $ = require('jquery'); // Adding JQuery library/requirements for HTTP requests

export default class Main extends React.Component {
  constructor(props) {  // props = parameters passed to the constructor (kind of global variable or object)
    super(props);       // super = refers to parent constructor (able to use "this." now)

    // "this.state" represents the rendered values, i.e. what’s currently on the screen, similar with "this.props"
    this.state = {
      fileTxt: '',
      filename: '',
      convertedFiles: [] // an empty array
    };

    // Class methods in JS are not bound by default
    // Binding in our constructor when we want to use "this." in a function callback
    // Applies when we call a function without "()". E.g. “onClick={...}” in our render()
    this.getUploadFileData = this.getUploadFileData.bind(this);
    this.handleFileChange = this.handleFileChange.bind(this);
    this.handleConvertedFileClick = this.handleConvertedFileClick.bind(this);
  }

  // Getting the uploaded .eml file data
  getUploadFileData(ev) {
    ev.preventDefault();            // Prevents the user to click a faulty link
    const data = new FormData();    // Fetch (see below), can accept a FormData object as a body

    // this.uploadInput.files[0], an array that stores all the files from the 'file' input
    // size/field = [0], the array needs only 1 element for 1 file input
    data.append('file', this.uploadInput.files[0]);

    // define fetch() methods to make a server call (fetching "/uploads") with POST method,
    // by setting content type with request data in the React
    fetch('http://127.0.0.1:5000/uploads', {
      method: 'POST',
      body: data,
    }).then((response) => response.json() // then, extract the JSON body content from the response
    )

  }

  // Fetching the "/uploads" URL by retrieving the converted files (the .txt files)
  handleFileChange(selectorFiles) {
    const data = new FormData();    // can accept a FormData object as a body
    data.append('file', selectorFiles[0]); // selectorFiles[0], an array that stores all the files from the 'file' input
    console.log("getUploadFileDat() & handleFileChange() executed") // tracking if the function is executed
    fetch('http://127.0.0.1:5000/uploads', {
      method: 'POST',
      body: data,
    }).then(res => {
      return res.json() // sends a JSON response composed of the specified data
    })
    .then(body => {
      let convertedFiles = this.state.convertedFiles // declare a variable that is limited to the scope of the statement
      convertedFiles.push(body.filename) // add the file's name into the array
      this.setState({ fileTxt: body.response, filename: body.filename, convertedFiles })
    }).catch(ex => {
        console.log(ex); // catches the exception and retrieve a message error through its reference, on the console
    });
  }

  // Switch .txt files straight forward, make a server call with GET method
  handleConvertedFileClick(file) {
    console.log(file)
    fetch('http://127.0.0.1:5000/load?filename='+file, { method: 'GET' }).then(res => {
      return res.json()
    })
    .then(body => {
      this.setState({ fileTxt: body.response })
    })
  }

  // Buttons - Upload and Display the file's content at once
  render() {
    
    return (
      <form onSubmit={this.getUploadFileData}>
        <div>
            {<input ref={(ref) => { this.uploadInput = ref; }} type="file" onChange={(e) => this.handleFileChange(e.target.files)}/>}
        </div>
        <div style={{ marginTop: '50px' }}>
          {this.state.convertedFiles.length ? (<h5>Converted Files</h5>) : <span /> }
          
          {this.state.convertedFiles.map((file,index) => (
            <button key={index} onClick={() => this.handleConvertedFileClick(file)}>{file.replace('_',' ')}.txt</button>
          ))}
        </div>

        <div style={{ marginTop: '50px' }}>
          {this.state.fileTxt.split('\n').map((line,index) => (
            <p key={index}> {line}</p>
          ))}
        </div>
        
      </form>
    );
  }
}
