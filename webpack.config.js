const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    mode: 'development', // Change to 'production' for optimized builds
    entry: './assets/src/js/app.js', // Entry point for your JS
    output: {
        path: path.resolve(__dirname, 'assets/dist/'), // Output folder
        filename: 'js/bundle.js', // Output JS file
    },
    module: {
        rules: [
            {
                test: /\.css$/, // Process CSS files
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'postcss-loader', // For Tailwind and autoprefixer
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