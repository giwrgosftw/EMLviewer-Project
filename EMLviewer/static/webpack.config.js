// Webpack.config.js - Bundles the modules' dependencies by creating our entry point (powerful loading)

const webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

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