const merge = require('webpack-merge');
const WebpackOnBuildPlugin = require('on-build-webpack');
const baseConfig = require("./webpack.base.js");

module.exports = merge(baseConfig, {
  mode: "development",
  watch: true,
  watchOptions: {
    poll: 5000
  },
  plugins: [
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
});
