module.exports = {
  mode: "development",
  watch: true,
  entry: {
    admin: "./static/js/admin.js",
    editor: "./static/js/editor.js"
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
          }
        ]
      }
    ]
  }
};
