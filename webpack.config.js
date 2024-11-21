const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    mode: 'development', // Change to 'production' for optimized builds
    entry: {
        app: ['./assets/src/js/app.js', './assets/src/js/utils.js'],  
        editor: './assets/src/js/editor.js', 

      },

    output: {
        filename: 'js/[name].bundle.js',
        path: path.resolve(__dirname, 'assets/dist/'), // Output folder
    },

    module: {
        rules: [
            {
                test: /\.css$/, // Process CSS files
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    // 'postcss-loader', // For Tailwind and autoprefixer
                ],
            },
        ],
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: 'css/app.css', // Output CSS file
        }),
    ],
};