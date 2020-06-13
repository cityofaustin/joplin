const merge = require('webpack-merge');
const baseConfig = require("./webpack.base.js");

module.exports = merge(baseConfig, {
  mode: "development",
  watch: true,
  watchOptions: {
    poll: 5000
  },
});
