// Main.jsx - 2nd front-end entry component, is connected with App.jsx
// What the user sees/interacts as here the front-end connects with the back-end

import React from 'react';
import { Button, Grid, Row, Col } from "react-bootstrap";

// var $ = require('jquery'); // Adding JQuery library/requirements for HTTP requests
var new_Filename;

export default class Main extends React.Component {
  constructor(props) {  // props = parameters passed to the constructor (kind of global variable or object)
    super(props);       // super = refers to parent constructor (able to use "this." now)

    this.state = {
      fileURL: '',     // Generate a new URL
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
    data.append('file', this.uploadInput.files[0]); // this.uploadInput.files[0] variable is an array stores all the files from the file input
                                                    // size/field [0] as the array needs only one element for one file input

    fetch('http://127.0.0.1:5000/uploads', {
      method: 'POST',
      body: data,
    }).then((response) => response.json() // extract the JSON body content from the response
    ).then((body) => {

        // The following 4-5 lines need to be changed by facing more special characters
        // new_Filename = this.uploadInput.files[0].name.replace(/[=[!&\/\\#,+()$~%'":*?<>{}] ]/g,'_').replace(/_{2,}/g,'_');
        new_Filename = this.uploadInput.files[0].name.split('(').join('');    // Bug fixed: if the filename includes "open bracket", delete it!
        new_Filename = new_Filename.split(')').join('');                      // Bug fixed: if the filename includes "close bracket", delete it!
        new_Filename = new_Filename.split(' ').join('_');                     // Bug fixed: if the filename includes spaces, then replaced them with "underscore"
        new_Filename = new_Filename.split('.eml').join('.txt');               // Read the new version of the uploaded file type .txt

        this.setState({ fileURL: `http://127.0.0.1:5000/uploads/`+ new_Filename });
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
