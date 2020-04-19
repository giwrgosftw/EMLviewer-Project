// Main.jsx - 2nd front-end entry component, is connected with App.jsx
// What the user sees/interacts as here the front-end connects with the back-end

import React from 'react';
import { Button, Grid, Row, Col } from "react-bootstrap";

var $ = require('jquery');
var no_Space_Filename;

export default class Main extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      fileURL: '',    // Generate a new URL
    };

    // Class methods in JS are not bound by default
    // Binding in our constructor when we want to use "this." in a call function
    // When we call a function without "()". E.g. onClick
    this.getUploadFileData = this.getUploadFileData.bind(this);
  }

  // Fetching the URL by retrieving the file's data
  getUploadFileData(ev) {
    console.log("getUploadFileDat() executed");
    ev.preventDefault();            // Prevents the user to click a faulty link
    const data = new FormData();    // Fetch (see below), can accept a FormData object as a body
    data.append('file', this.uploadInput.files[0]);

    fetch('http://127.0.0.1:5000/uploads', {
      method: 'POST',
      body: data,
    }).then((response) => response.json()
    ).then((body) => {
        no_Space_Filename = this.uploadInput.files[0].name.split('(').join('');    // Bug fixed: if the filename includes "open bracket", delete it!
        no_Space_Filename = no_Space_Filename.split(')').join('');                 // Bug fixed: if the filename includes "close bracket", delete it!
        no_Space_Filename = no_Space_Filename.split(' ').join('_');                // Bug fixed: if the filename includes spaces, then replaced them with "underscore"
        no_Space_Filename = no_Space_Filename.split('.eml').join('.txt');          // Read the new version of the uploaded file type .txt
        this.setState({ fileURL: `http://127.0.0.1:5000/uploads/`+ no_Space_Filename });
     }).catch(ex => {
        console.log(ex);
    });

  }

  // Buttons - Upload and Display the file's content
  render() {
    return (
      <form onSubmit={this.getUploadFileData}>
        <div>
            {<input ref={(ref) => { this.uploadInput = ref; }} type="file" />}
        </div>
        <br />
        <div>
	        <Button bsSize="large" bsStyle="primary" onClick={this.getUploadFileData}>
		     Upload!
		    </Button>
        </div>
        <div>
         <Button>
            <a href={this.state.fileURL} target="_blank"> Display!</a>
         </Button>
        </div>
      </form>
    );
  }
}
