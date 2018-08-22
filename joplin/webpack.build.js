var merge = require('webpack-merge');
var baseConfig = require("./webpack.base.js");

module.exports = merge(baseConfig, {
  mode: "production"
});
