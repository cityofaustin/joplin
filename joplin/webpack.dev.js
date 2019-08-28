var merge = require('webpack-merge');
var baseConfig = require("./webpack.base.js");

module.exports = merge(baseConfig, {
  mode: "development",
  watch: true,
  watchOptions: {
    poll: 5000
  },
});
