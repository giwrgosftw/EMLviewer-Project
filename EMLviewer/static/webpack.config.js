// Webpack.config.js - Bundles the modules' dependencies by creating our entry point (powerful loading)

const webpack = require('webpack');
const fs = require('fs-extra');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

// Fix the favicon bug, copy the favicon.ico to dist folder which is readable by html
async function copyFiles () {
  try {
    await fs.copy(__dirname + '/images/favicon.ico', __dirname + '/dist/favicon.ico')
    console.log('success!')
  } catch (err) {
    console.error(err)
  }
}

const config = {
    entry:  __dirname + '/js/index.jsx',
    output: {
        path: __dirname + '/dist',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: [".js", ".jsx", ".css"]
    },
    module: {
        rules: [
            {
				test: /\.jsx?/,
				exclude: /node_modules/,   // Ensure that Babel converter does not transform any of the node_modules (support special keywords and features e.g. scripts)
				use: 'babel-loader'        // Converts jsx to js as HTML does not understand jsx
			},
			{
				test: /\.css$/,
				use: ExtractTextPlugin.extract({
					fallback: 'style-loader',
					use: 'css-loader',
				})
			},
			{
				test: /\.(png|svg|jpg|gif)$/,
				use: 'file-loader'
			}
        ]
    },
	plugins: [
		new ExtractTextPlugin('styles.css'),
	]
};

module.exports = config;
copyFiles();