const webpack = require('webpack');
const merge = require('webpack-merge');
const baseConfig = require("./webpack.base.js");
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

module.exports = merge(baseConfig, {
  mode: "production",
  optimization: {
    minimizer: [
      new UglifyJsPlugin({
        sourceMap: true,
      }),
    ]
  }
});
