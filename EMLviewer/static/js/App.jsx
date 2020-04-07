// App.jsx - is connected with Index.jsx (OUTPUT POINT)
// Interacts with the css folder, background image and Main.jsx

import React from "react";
import Main from "./Main";
import { PageHeader } from "react-bootstrap";

require('../css/fullstack.css');
var $ = require('jquery'); // Adding JQuery library/requirements for HTTP requests

import HeaderBackgroundImage from '../images/header.jpg';

// Always have to import+export the react files in order to show what they do
export default class App extends React.Component {
	constructor(props) {
		super(props); // props are parameters that passed into the constructor, are public and re-rendered the UI after any update state
	}

	// Insert the background image
	addHeaderImg() {
		let headerBg = new Image();
		headerBg.src = HeaderBackgroundImage;
	}

    // Display background image and Main.jsx content
	render () {
        return (
			<PageHeader>
				<div className='header-contents'>
				{this.addHeaderImg()}
				<Main />
				</div>
			</PageHeader>
		);
    }
}