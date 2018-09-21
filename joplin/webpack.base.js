var BundleTracker = require("webpack-bundle-tracker");
var path = require("path");

// Using this example to save some config copy pasta
// https://simonsmith.io/organising-webpack-config-environments/

module.exports = {
  entry: {
    admin: "./js/admin.js",
    editor: "./js/editor.js",
    createContentModal: './js/CreateContentModal/index.js'
  },
  module: {
    rules: [
        {
            test: /\.js?$/,
            exclude: /node_modules/,
            loader: 'babel-loader',
            query: {
              // presets: ['react', 'es2015', 'react-hmre'],
              plugins: ['transform-class-properties']
            }
        },
        {
            test: /\.scss$/,
            loaders: [
              "style-loader", // creates style nodes from JS strings
              "css-loader", // translates CSS into CommonJS
              "sass-loader" // compiles Sass to CSS
            ]
        },
        {
            test: /\.(png|jp(e*)g|svg)$/,
            use: [{
                loader: 'url-loader',
                options: {
                    limit: 8000, // Convert images < 8kb to base64 strings
                    name: 'images/[hash]-[name].[ext]'
                }
            }]
        }
    ],
  },
  output: {
    path: path.resolve("./static/webpack_bundles/"),
    filename: "[name]-[hash].js"
  },
  plugins: [
    new BundleTracker({
      path: __dirname,
      filename: "./static/webpack-stats.json"
    })
  ]
};
