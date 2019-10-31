const path = require("path");
const fs = require("fs");
const BundleTracker = require("webpack-bundle-tracker");
const WebpackOnBuildPlugin = require('on-build-webpack');

// Using this example to save some config copy pasta
// https://simonsmith.io/organising-webpack-config-environments/

const buildDir = path.resolve(__dirname, "./static/webpack_bundles/")

module.exports = {
  entry: {
    admin: path.resolve(__dirname, "./js/admin.js"),
    editor: path.resolve(__dirname, "./js/editor.js"),
    createContentModal: path.resolve(__dirname, "./js/CreateContentModal/index.js"),
    janisBranchSettings: path.resolve(__dirname, "./js/janisBranchSettings.js"),
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
    path: buildDir,
    filename: "[name]-[hash].js"
  },
  plugins: [
    new BundleTracker({
      path: path.resolve(__dirname, "./static/"),
      filename: "webpack-stats.json"
    }),
    new WebpackOnBuildPlugin(function(stats) {
      // Deletes old bundles once new ones are created
      const hashtest = new RegExp(`${stats.hash}.js$`)
      fs.readdir(buildDir, (err, files) => {
        files.forEach(file => {
          if (!file.match(hashtest)) {
            fs.unlinkSync(path.resolve(buildDir, file))
          }
        })
      })
    })
  ]
};
