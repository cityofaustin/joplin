var BundleTracker = require("webpack-bundle-tracker");
var path = require("path");

module.exports = {
  mode: "production",
  entry: {
    admin: "./js/admin.js",
    editor: "./js/editor.js",
    createContentModal: './js/create-content-modal.js'
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          {
            loader: "style-loader" // creates style nodes from JS strings
          },
          {
            loader: "css-loader" // translates CSS into CommonJS
          },
          {
            loader: "sass-loader" // compiles Sass to CSS
          },
          {
            loader: 'babel-loader', // gives us JSX for React
          }
        ]
      }
    ]
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
