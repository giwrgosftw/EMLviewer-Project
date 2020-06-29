// Index.jsx - Our Front-end environment (ENTRY POINT)
// Is connected with index.html (keyword: content)

import React from "react"; // import React Library in order to use react.js
import ReactDOM from "react-dom"; // provide render() method, we can now render our react component/element to the DOM
import App from "./App"; // import our App in the index.jsx which communicate with the index.html

// We want to render to our index.html using the 'content' as connection key
ReactDOM.render(<App />, document.getElementById("content"));
