// App.jsx - is connected with Index.jsx (OUTPUT POINT)
// Interacts with the css folder, background image and Main.jsx

import React from "react";
import Main from "./Main";
import '../css/fullstack.css' // declare our css style

// require('../css/fullstack.css');
// var $ = require('jquery'); // Adding JQuery library/requirements for HTTP requests

// Always have to import+export the react files in order to show what they do
export default class App extends React.Component {
	constructor(props) {
		super(props); // props are parameters that passed into the constructor
		              // are public and re-rendered the UI after any update state
	}

    // Display background image and Main.jsx content with a specific format/style
	render () {
        return (
        <div className='page-header'>
		    <div style={{ width: '80vw', marginLeft: 'auto', marginRight: 'auto', minHeight: '99vh', marginTop:'10vh', display: 'flex',  }}>
				<Main />
			</div>
		</div>
		);
    }

}
